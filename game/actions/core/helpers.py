import inspect
from typing import get_type_hints


def python_type_to_json_type(py_type):
    if py_type in (int,):
        return "integer"
    if py_type in (float,):
        return "number"
    if py_type in (bool,):
        return "boolean"
    if py_type in (list,):
        return "array"
    if py_type in (dict,):
        return "object"
    return "string"


def get_tool_metadata(
    func,
    tool_name=None,
    description=None,
    parameters_override=None,
    terminal=False,
    tags=None,
):
    tool_name = tool_name or func.__name__

    description = description or (
        func.__doc__.strip()
        if func.__doc__
        else "No description provided."
    )

    if parameters_override is None:
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)

        parameters = {
            "type": "object",
            "properties": {},
            "required": [],
        }

        for name, param in signature.parameters.items():
            if name in ("action_context", "action_agent"):
                continue

            py_type = type_hints.get(name, str)
            parameters["properties"][name] = {
                "type": python_type_to_json_type(py_type)
            }

            if param.default is inspect.Parameter.empty:
                parameters["required"].append(name)

    else:
        parameters = parameters_override

    return {
        "tool_name": tool_name,
        "description": description,
        "parameters": parameters,
        "function": func,
        "terminal": terminal,
        "tags": tags or [],
    }
