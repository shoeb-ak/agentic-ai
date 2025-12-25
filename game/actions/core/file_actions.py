import os
from typing import Dict
from game.actions.core.decorators import register_tool

@register_tool(tags=["file_operations", "list"])
def list_files(dir_path: str) -> list:
    return os.listdir(dir_path)

@register_tool(tags=["file_operations", "read"])
def read_file(file_name: str) -> str:
    """Reads and returns the content of a file.

    Args:
        file_name: Name of the file
    """
    with open(file_name, 'r') as f:
        return f.read()

@register_tool(tags=["file_operations", "search"])
def search_in_file(file_name: str, search_term: str) -> list:
    """Searches for a term in a specific file.

    Args:
        file_name: Name of the file
        search_term: Term to search in the file
    """
    results = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if search_term in line:
                results.append((i+1, line.strip()))
    return results

@register_tool(tags=["file_operations", "write"])
def write_output_file(
    filename: str,
    content: str,
    output_dir: str = "output"
) -> Dict[str, str]:
    """
    Write content to a file inside the output directory.
    Creates the directory if it does not exist.

    Args:
        filename: Name of the file
        content: File content to write
        output_dir: Target directory (default: output)

    """

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "output_path": file_path,
        "bytes_written": len(content.encode("utf-8"))
    }
