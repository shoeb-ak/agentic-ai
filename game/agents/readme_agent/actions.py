from game.actions.action import Action
from game.actions.registry import ActionRegistry
from game.actions.core.actions_registry import core_registry
from typing import List
import os

def list_project_files(dir_path: str) -> List[str]:
    return sorted([file for file in os.listdir(dir_path) if file.endswith(".py")])

registry = ActionRegistry()

registry.merge(core_registry)

registry.register(Action(
        name="list_project_files",
        function=list_project_files,
        description="Lists all files in the project.",
        parameters={
            "type": "object", 
            "properties": {
                "dir_path": {"type": "string"}
            }, 
            "required": ["dir_path"]
        },
        terminal=False
    ))
