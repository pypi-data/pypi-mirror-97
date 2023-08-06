"""Mardown viewers for Module and Port."""
from cosapp.ports.port import ExtensiblePort
from cosapp.systems import System


def port_to_md(port: ExtensiblePort) -> str:
    """Returns the representation of this port variables in Markdown format.

    Parameters
    ----------
    port : ExtensiblePort
        Port to describe
        
    Returns
    -------
    str
        Markdown formatted representation
    """
    return "\n".join([
        f"- {value!r}" for value in port.get_details().values()
    ])


def system_to_md(system: System) -> str:
    """Returns the representation of a system in Markdown format.

    Parameters
    ----------
    system : System
        System to describe

    Returns
    -------
    str
        Markdown formatted representation
    """
    doc = list()
    if len(system.tags) > 0:
        doc.extend(["", f"**Tags**: {list(system.tags)!s}", ""])

    if len(system.children) > 0:
        doc.extend(["", "### Child components", ""])
        for name, child in system.children.items():
            doc.append(f"- `{name}`: {type(child).__name__}")

    if hasattr(system, 'residues') and len(system.residues) > 0:
        doc.extend(["", "### Residues", ""])
        doc.append(", ".join([f"`{key}`" for key in system.residues]))

    common_inputs = [System.INWARDS]
    common_outputs = [System.OUTWARDS]
    has_ports = len(system.inputs) + len(system.outputs) > len(common_inputs) + len(common_outputs)

    if has_ports:
        doc.extend(["", "### Ports", ""])

        def dump_port_data(header, port_dict, common_ports):
            if len(port_dict) <= len(common_ports):
                return
            doc.extend(["", f"#### {header.title()}", ""])
            for name, port in filter(lambda item: item[0] not in common_ports, port_dict.items()):
                doc.append(f"- `{name}`:")
                doc.extend([f"  {line}" for line in port_to_md(port).splitlines()])

        dump_port_data("inputs", system.inputs, common_inputs)
        dump_port_data("outputs", system.outputs, common_outputs)

    for name in common_inputs + common_outputs:
        if len(system[name]) > 0:
            doc.extend(["", f"#### {name.capitalize()}", ""])
            doc.append(port_to_md(system[name]))

    return "\n".join(doc)
