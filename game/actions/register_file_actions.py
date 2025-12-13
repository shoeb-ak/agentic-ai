from .registry import ActionRegistry
from .action import Action
from .file_actions import list_files, read_file, search_in_file, should_terminate

registry = ActionRegistry()

registry.register(Action(
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

registry.register(Action(
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

registry.register(Action(
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

registry.register(Action(
    name="should_terminate",
    function=should_terminate,
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

