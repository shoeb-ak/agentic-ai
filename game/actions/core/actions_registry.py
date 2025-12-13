from game.actions.registry import ActionRegistry
from game.actions.action import Action
from game.actions.core.file_actions import list_files, read_file, search_in_file
from game.actions.core.terminate_action import terminate

core_registry = ActionRegistry()

core_registry.register(Action(
    name="list_files",
    function=list_files,
    description="List all files in the current directory",
    parameters=
        {"type": "object", "properties": {
            "dir_path": {"type": "string"}
        }, 
        "required": ["dir_path"]
    }
))

core_registry.register(Action(
    name="read_file",
    function=read_file,
    description="Read the contents of a specific file",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {"type": "string"}
        },
        "required": ["file_name"]
    }
))

core_registry.register(Action(
    name="search_in_file",
    function=search_in_file,
    description="Search for a term in a specific file",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "search_term": {"type": "string"}
        },
        "required": ["file_name", "search_term"]
    }
))

core_registry.register(Action(
    name="terminate",
    function=terminate,
    description="Terminate the conversation with a helpful summary",
    parameters={
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    },
    terminal = True
))

