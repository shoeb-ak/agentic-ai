from typing import List
import os

from game.actions.core.decorators import register_tool


@register_tool(tags=["readme"])
def list_project_files(dir_path: str) -> List[str]:
    """Lists all Python files in the project directory."""
    return sorted(
        file for file in os.listdir(dir_path)
        if file.endswith(".py")
    )
