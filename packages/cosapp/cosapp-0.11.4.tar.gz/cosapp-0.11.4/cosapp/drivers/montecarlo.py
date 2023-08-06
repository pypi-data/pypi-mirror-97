import logging
from collections import OrderedDict
from typing import Any, Iterable, List, Optional, Set, Union

import numpy

from cosapp.core.numerics import sobol_seq
from cosapp.ports.port import ExtensiblePort, PortType
from cosapp.drivers.abstractsetofcases import AbstractSetOfCases
from cosapp.drivers.abstractsolver import AbstractSolver
from cosapp.utils.helpers import check_arg

logger = logging.getLogger(__name__)


# TODO linearization does not support multipoint cases
# TODO Does not work for vector variables (at least partially connected one)
# TODO Does it work if a subsystem mutates to higher/lower fidelity
# TODO We don't forbid using an unknown
class MonteCarlo(AbstractSetOfCases):
    """
    This driver execute a MonteCarlo simulation on its system.
    """

    __slots__ = (
        'draws', 'linear', 'random_variables', 'responses', 'solver', 'reference_case_solution',
        'X0', 'Y0', 'A', 'perturbations'
    )

    def __init__(self,
        name: str,
        owner: "Optional[cosapp.systems.System]" = None,
        **kwargs
    ) -> None:
        """Initialize a driver

        Parameters
        ----------
        name: str, optional
            Name of the `Module`
        owner : System, optional
            :py:class:`~cosapp.systems.system.System` to which this driver belong; default None
        **kwargs : Dict[str, Any]
            Optional keywords arguments
        """
        super().__init__(name, owner, **kwargs)
        self.draws = 200  # type: int
            # desc="Number of cases performed for Montecarlo calculations."
        self.linear = False  # type: bool
            # desc="True for linearisation of system before Montecarlo calculation. Default False."

        self.random_variables = OrderedDict()  # type: Dict[str, Tuple[VariableReference, Optional[Connector], Distribution]]
            # desc="Random variables in the system."
        self.responses = list()  # type: List[str]
            # We need a list as set is not ordered
            # desc="Variable names to study through Monte Carlo calculations."
        self.solver = None  # type: Optional[AbstractSolver]
            # desc="Solver acting. Used for re-init of case."
        self.reference_case_solution = dict()  # type: Dict[str, float]

        self.X0 = None  # type: Optional[numpy.ndarray]
            # desc="Vector of imposed disturbed values"
        self.Y0 = None  # type: Optional[numpy.ndarray]
            # desc="Vector of output evaluated disturbed values."            
        self.A = None  # type: Optional[numpy.ndarray]
            # desc="Matrice of influence of imposed disturbed values on results."
        self.perturbations = None  # type: Optional[numpy.ndarray]
            # desc="Array of perturbations applied on the system."

    def add_random_variable(self, names: Union[str, Iterable[str]]) -> None:
        """Add variable to be perturbated.

        The perturbation distribution is defined by the variable distribution details.

        ..
            from cosapp.core.numerics.distribution import Normal

            port.get_details('my_variable').distribution = Normal(worst=0.0, best=5.0)

        Parameters
        ----------
        names : Union[str, Iterable[str]]
            List of variables to be perturbated
        """
        # TODO it should be possible to set the distribution directly

        def add_unique_input_var(name: str):
            self.check_owner_attr(name)
            ref = self.owner.name2variable[name]
            port = ref.mapping

            if not isinstance(port, ExtensiblePort):
                raise TypeError(f"{name!r} is not a variable.")

            if port.direction != PortType.IN:
                raise TypeError(
                    f"{ref.key!r} is not an input variable of {port.contextual_name!r}"
                )

            distribution = port.get_details(ref.key).distribution
            if distribution is None:
                raise ValueError(
                    f"No distribution specified for '{port.contextual_name}.{ref.key}'"
                )

            # Test if the variable is connected
            connection = None
            if port.owner.parent is not None:
                connectors = port.owner.parent.connectors.values()
                for connector in filter(lambda c: c.sink is port, connectors):
                    if ref.key in connector.variable_mapping:
                        connection = connector
                        break

            self.random_variables[name] = (ref, connection, distribution)

        check_arg(names, 'names', (str, set, list))

        if isinstance(names, str):
            add_unique_input_var(names)
        else:
            for name in names:
                check_arg(name, name + " in 'names'", str)
                add_unique_input_var(name)

    def add_response(self, name: Union[str, Iterable[str]]) -> None:
        """Add a variable for which the statistical response will be calculated.

        Parameters
        ----------
        name : Union[str, Iterable[str]]
            List of variable names to add
        """
        def add_unique_response_var(name: str):
            self.check_owner_attr(name)
            if name not in self.responses:
                self.responses.append(name)

        check_arg(name, 'name', (str, set, list))

        if isinstance(name, str):
            add_unique_response_var(name)
        else:
            for n in name:
                check_arg(n, n + " in 'name'", str)
                add_unique_response_var(n)

    def _build_cases(self) -> None:
        """Build the list of cases to run during execution
        """
        self.cases = sobol_seq.i4_sobol_generate(len(self.random_variables), self.draws)

    def _precompute(self):
        """Save reference and build cases."""
        n_input = len(self.random_variables)
        n_output = len(self.responses)

        self.run_children()

        self.solver = None
        for child in self.children.values():
            if isinstance(child, AbstractSolver):
                self.solver = child

        if self.solver:
            self.reference_case_solution = child.save_solution()

        self._build_cases()

        if self.linear:  # precompute linear system
            if len(self.responses) == 0:
                raise ValueError("You need to define response variables to use MonteCarlo linear mode.")
            self.X0 = numpy.zeros(n_input)
            self.Y0 = numpy.zeros(n_output)
            self.A = numpy.zeros((n_output, n_input))

            # reference for influence matrix computation through center differentiation scheme
            for i, name in enumerate(self.random_variables):
                self.X0[i] = self.owner[name]
            for j, name in enumerate(self.responses):
                self.Y0[j] = self.owner[name]

            variation = 0.5 * (numpy.max(self.cases, axis=0) - numpy.min(self.cases, axis=0))
            for i, input_name in enumerate(self.random_variables):
                self.owner[input_name] = self.X0[i] + variation[i]
                self.run_children()

                for j, response_name in enumerate(self.responses):
                    self.A[j, i] = 0.5 * (self.owner[response_name] - self.Y0[j]) / variation[i]

                self.owner[input_name] = self.X0[i] - variation[i]
                self.run_children()

                for j, response_name in enumerate(self.responses):
                    self.A[j, i] -= 0.5 * (self.owner[response_name] - self.Y0[j]) / variation[i]

                # Restore system value
                self.owner[input_name] = self.X0[i]

            for j, name in enumerate(self.responses):
                self.Y0[j] = self.owner[name]

    def _precase(self, case_idx, case):
        """Hook to be called before running each case.
        
        Parameters
        ----------
        case_idx : int
            Index of the case
        case : Any
            Parameters for this case
        """
        super()._precase(case_idx, case)

        # Set perturbation
        self.perturbations = numpy.zeros(len(self.random_variables))
        for i, params in enumerate(self.random_variables.values()):
            ref, connector, distribution = params
            self.perturbations[i] = distribution.draw(case[i])
            if connector is None:
                ref.value += self.perturbations[i]
            else:
                connector.set_perturbation(ref.key, self.perturbations[i])

        if len(self.reference_case_solution) > 0:
            self.solver.load_solution(self.reference_case_solution)

    def compute(self) -> None:
        """Contains the customized `Module` calculation, to execute after children.
        """
        for case_idx, case in enumerate(self.cases):
            if len(case) > 0:
                self._precase(case_idx, case)
                if self.linear:
                    self.__run_linear()
                else:
                    self.run_children()
                self._postcase(case_idx, case)

    def __run_linear(self) -> None:
        """Approximate MonteCarlo simulation using partial derivatives matrix."""
        # TODO this is not great as we set variables in the system breaking its consistency.
        if len(self.responses) > 0:
            X = numpy.zeros(len(self.random_variables))
            for i, name in enumerate(self.random_variables):
                self.X0[i] = self.owner[name]

            Y = self.Y0 + numpy.matmul(self.A, X - self.X0)

            for j, name in enumerate(self.responses):
                self.owner[name] = Y[j]

    def _postcase(self, case_idx: int, case: Any):
        """Hook to be called before running each case.
        
        Parameters
        ----------
        case_idx : int
            Index of the case
        case : Any
            Parameters for this case
        """
        # Store the results
        super()._postcase(case_idx, case)

        # Remove the perturbation
        for i, params in enumerate(self.random_variables.values()):
            ref, connector = params[:2]
            if connector is None:
                ref.value -= self.perturbations[i]
            else:
                connector.set_perturbation(ref.key, -self.perturbations[i])
