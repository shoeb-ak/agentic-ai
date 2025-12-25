from game.actions.core.helpers import get_tool_metadata
from game.actions.core.actions_registry import register_tool_metadata

def register_tool(
    tool_name=None,
    description=None,
    parameters_override=None,
    terminal=False,
    tags=None,
):
    """
    A decorator to dynamically register a function in the tools dictionary with its parameters, schema, and docstring.

    Parameters:
        tool_name (str, optional): The name of the tool to register. Defaults to the function name.
        description (str, optional): Override for the tool's description. Defaults to the function's docstring.
        parameters_override (dict, optional): Override for the argument schema. Defaults to dynamically inferred schema.
        terminal (bool, optional): Whether the tool is terminal. Defaults to False.
        tags (List[str], optional): List of tags to associate with the tool.

    Returns:
        function: The wrapped function.
    """
    def decorator(func):
        metadata = get_tool_metadata(
            func=func,
            tool_name=tool_name,
            description=description,
            parameters_override=parameters_override,
            terminal=terminal,
            tags=tags,
        )
        register_tool_metadata(metadata)
        return func
    return decorator
