import numpy
import collections
import pickle
import pandas
import logging
import warnings
from numbers import Number
from collections import OrderedDict
from typing import Any, Dict, Iterable, NamedTuple, NoReturn, Union, Optional, List

from cosapp.utils.helpers import check_arg
from cosapp.utils.logging import LogLevel
from cosapp.utils.find_variables import find_variables, make_wishlist, natural_varname
from cosapp.ports.enum import PortType


logger = logging.getLogger(__name__)


class SystemSurrogateState(NamedTuple):
    """Named tuple containing internal state data of a SystemSurrogate object"""
    doe_in: pandas.DataFrame
    doe_out: Union[pandas.DataFrame, OrderedDict]
    model: Any
    doe_out_sizes: OrderedDict


class SystemSurrogate:
    """
    Class representing a surrogate model trained from the outputs of an owner system.
    Once the surrogate is created, it supersedes (whenever activated) the behaviour of
    `System.compute()`. 
    """
    __slots__ = ('__owner', '__state', '__need_doe')

    def __init__(self,
        owner: "cosapp.systems.System",
        data_in: Union[pandas.DataFrame, Dict[str, Any]],
        model: type,
        data_out: Optional[Union[pandas.DataFrame, Dict[str, Any]]] = None,
        postsynch: Union[str, List[str]] = '*',
        *args, **kwargs
    ):
        # CHECK ARGS
        from cosapp.systems import System
        check_arg(owner, 'owner', System)
        check_arg(data_in, 'data_in', (pandas.DataFrame, dict))
        check_arg(data_out, 'data_out', (pandas.DataFrame, dict, type(None)))
        if model is not None:
            check_arg(model, 'model', type,
                lambda m: all(hasattr(m, attr) for attr in ('train', 'predict'))
            )
        postsynch = make_wishlist(postsynch, 'postsynch')

        if owner is not None:
            logger.debug(f"Initialize surrogateclass for System {owner.name!r}, data_in as {data_in} and model as {model}")

        # BUILD INTERN DATA
        self.__owner = owner
        self.__need_doe = data_out is None
        
        doe_in = pandas.DataFrame.from_dict(data_in) if isinstance(data_in, dict) else data_in
        doe_out = self.__init_doe_out(data_out, postsynch)
        model_obj = None if model is None else model(*args, **kwargs)
        self.__state = SystemSurrogateState(doe_in, doe_out, model_obj, OrderedDict())
        
        # TRAINING
        empty = any(obj is None for obj in (owner, model_obj)) or len(data_in) == 0
        if not empty:
            self.__check_unknowns_and_transients()
            self.__prepare_and_train()

        logger.debug(f"surrogateclass initialized")

    @property
    def state(self)-> SystemSurrogateState:
        return self.__state

    @property
    def owner(self)-> "cosapp.systems.System":
        return self.__owner

    @property
    def synched_outputs(self) -> List[str]:
        """List[str]: list of synchronized output variable names"""
        return list(self.__state.doe_out_sizes.keys())

    def __init_doe_out(self, data_out, postsynch) -> "OrderedDict[str, List]":
        doe_out = OrderedDict()
        if isinstance(data_out, pandas.DataFrame):
            doe_out = data_out.to_dict(into=OrderedDict)
        elif data_out is not None:
            doe_out = OrderedDict(data_out)
        elif self.owner is not None:
            watched = self.__get_owner_connections()
            varlist = watched.keys()
            if '*' not in postsynch:
                owner = self.owner
                def writeable(var) -> bool:
                    try:
                        owner[var] = owner[var]
                    except AttributeError:
                        return False
                    else:
                        return True
                varlist = find_variables(owner,
                        includes=postsynch,
                        excludes=None,
                        inputs=False,
                    )
                varlist = set(filter(writeable, varlist))
                # Make sure varlist contains at least owner system outputs
                for port, output in owner.outputs.items():
                    varlist |= set(natural_varname(f"{port}.{var}") for var in output)
            doe_out = OrderedDict((var, []) for var in varlist)
        return doe_out

    def __get_doe_out_sizes(self) -> None:
        state = self.__state
        owner = self.__owner
        doe_out_sizes = OrderedDict.fromkeys(state.doe_out.keys(), None)
        pos = 0
        for var in doe_out_sizes:
            size = 0
            value = owner[var]
            if isinstance(value, Number):
                size = 1
            elif isinstance(value, numpy.ndarray):
                size = value.size
            else:
                raise TypeError(
                    f"Unsupported data type {type(value).__name__} for {owner.name}.{var}"
                )
            doe_out_sizes[var] = (pos, size)
            pos += size
        self.__state = SystemSurrogateState(
            state.doe_in,
            state.doe_out,
            state.model,
            doe_out_sizes,
        )

    def __format_outputs(self) -> numpy.ndarray:
        logger.debug(f"Reshaping outputs")
        doe_length = len(self.__state.doe_in)
        doe_out = self.__state.doe_out
        reshaped_outputs = []
        for k in range(doe_length):
            reshaped_outputs.append(
                list(value[k] for value in doe_out.values())
            )
        reshaped_outputs = numpy.asarray(list(list(flatten(el)) for el in reshaped_outputs))
        # logger.debug(f"Reshaped outputs are now numpy.ndarray and are: {reshaped_outputs}")
        return reshaped_outputs

    def __format_inputs(self) -> numpy.ndarray:
        logger.debug(f"Reshaping input data")
        res = []
        for couple_values in self.__state.doe_in.values:
            res.append(list(flatten(couple_values)))
        return numpy.asarray(res)

    def __set_and_execute(self) -> None:
        logger.debug(f"Setting and executing in order to build data for training")
        owner = self.__owner
        doe_out = self.__state.doe_out
        for i, row in self.state.doe_in.iterrows():
            logger.log(LogLevel.FULL_DEBUG, f"Setting {owner.name!r} input values (DOE row #{i})")
            for var, value in row.items():
                owner[var] = value
            owner.run_drivers()
            # add tracked output data to doe_out
            for var in doe_out:
                doe_out[var].append(owner[var])

    def add_data(self, newdoe: pandas.DataFrame) -> NoReturn:
        # TODO: Should merge input lists when matching names (not working yet)
        # self.__state = SystemSurrogateState(
        #     self.__state.doe_in,
        #     self.__state.doe_out,
        #     self.__state.model,
        #     OrderedDict(),
        # )
        raise NotImplementedError()

    def __prepare_and_train(self) -> None:
        logger.debug(f"Preparing and training function")
        if len(self.state.doe_out) == 0:
            raise ValueError(
                f"Cannot train surrogate model: no output found in System {self.owner.name!r}"
            )
        self.__get_doe_out_sizes()
        if self.__need_doe:
            self.__set_and_execute()
        x = self.__format_inputs()
        y = self.__format_outputs()
        self.__train_model(x, y)

    def __train_model(self, x, y) -> None:
        model = self.__state.model
        logger.debug(f"Training model {model} with \n\tX = {x}\n\tY = {y}")
        model.train(x, y)
        logger.debug(f"Model {model} trained")

    def predict(self, x):
        return self.__state.model.predict(x).reshape(1, -1)[0]

    def compute(self) -> None:
        logger.debug(f"Start meta_compute() instead of {self.owner.name}.compute().")
        inputs = self.__get_owner_inputs()
        outputs = self.predict(inputs)
        self.__set_owner_outputs(outputs)
        logger.debug(f"meta_compute() done")

    def __get_owner_inputs(self) -> numpy.ndarray:
        owner = self.owner
        logger.debug(f"Getting current inputs of system {owner.name}")
        inputs = list(flatten(owner[var] for var in self.__state.doe_in.columns))
        logger.debug(f"Detected input values: {inputs}")
        return numpy.asarray(inputs)

    def __set_owner_outputs(self, np_outputs: numpy.ndarray) -> None:
        owner = self.__owner
        logger.log(LogLevel.FULL_DEBUG, f"Post-synchronize outputs of {owner.name}")
        for var, (pos, size) in self.__state.doe_out_sizes.items():
            if size == 1:
                owner[var] = np_outputs[pos]
            elif size > 1:
                owner[var].ravel()[:] = np_outputs[pos : pos + size]

    def dump(self, filename: str) -> None:
        """Dump current state to file"""
        logger.debug(f"Dumping metamodel in {filename}")
        with open(filename, 'wb') as fp:
            pickle.dump(self.__state, fp)

    @classmethod
    def load(cls, owner: "cosapp.systems.System", filename: str) -> "SystemSurrogate":
        """Load system surrogate from file"""
        logger.debug(f"Loading metamodel from {filename}")
        from cosapp.systems import System
        check_arg(owner, 'owner', System)
        with open(filename, 'rb') as fp:
            state = pickle.load(fp)
        if not isinstance(state, SystemSurrogateState):
            raise TypeError("cannot load object")
        obj = cls(owner, data_in={}, model=None)
        obj.__state = state
        return obj

    def __check_unknowns_and_transients(self) -> None:
        state = self.state
        unknowns = get_unknows_transients(self.__owner)
        unsolvable_unknows = set(unknowns).difference(state.doe_out.keys())
        trained_unknowns = unsolvable_unknows.issubset(state.doe_in.keys())
        if not trained_unknowns:
            message = "The following unknowns/transients are not part of the training set; "\
                "future attempts to compute them with a driver may fail:"
            for name in unknowns.difference(state.doe_in.keys()):
                message += f"\n\t- {name}"
            warnings.warn(message)

    def __get_owner_connections(self) -> "OrderedDict[str, list]":
        return get_dependant_connections(self.__owner)


def flatten(iterable: Iterable) -> Iterable:
    for elem in iterable:
        if isinstance(elem, collections.abc.Iterable) and not isinstance(elem, str): 
            yield from flatten(elem)
        else:
            yield elem


def get_dependant_connections(system, head_system=None) -> Dict[str, list]:
    """
    This function returns a dictionnary mapping variable names to a port direction.
    Keys are absolute paths to connected inputs and all outputs.
    Values are owner port direction.
    """
    logger.debug(f"Starting recursive getter of connected inputs and all outputs on {system.name}")
    result = dict()
    prefix = ""

    if head_system is None:
        head_system = system
    elif system is not head_system:
        prefix = f"{head_system.get_path_to_child(system)}."
        for list_connectors in system.parent._connectors.values():
            for connector in list_connectors:
                sink = connector.sink
                mapping = connector.variable_mapping
                logger.debug(f"Detecting connector {connector} with sink {sink.name!r}")
                if sink in system.inputs.values():
                    for portvariable in mapping:
                        key = f"{prefix}{sink.name}.{portvariable}"
                        result[key] = PortType.IN
                        logger.debug(f"Add {key} to list of connected inputs")

    for output in system.outputs.values():
        logger.debug(f"Checking output {output}.")
        for portvariable in output:
            key = f"{prefix}{output.name}.{portvariable}"
            logger.debug(f"Add {key} to list of outputs")
            result[key] = PortType.OUT
    if system.is_standalone():
        unknowns = system.get_unsolved_problem().unknowns
        for unknown in unknowns:
            key = f"{prefix}{unknown}"
            result[key] = PortType.IN
            logger.debug(f"Add {key} to list of unknowns")
    for child in system.children.values():
        logger.debug(f"Targeted child of recursive getter of connected inputs and all outputs is {child}")
        child_dict_path_str = get_dependant_connections(child, head_system)
        result.update(child_dict_path_str)
    return result


def get_unknows_transients(system: "cosapp.systems.System") -> set:
    res = set()
    problem = system.get_unsolved_problem()
    for collection in (problem.unknowns, problem.transients):
        res |= set(collection)
    return res
