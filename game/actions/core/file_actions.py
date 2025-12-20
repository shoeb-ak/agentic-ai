import os
from typing import Dict

def list_files(dir_path: str) -> list:
    return os.listdir(dir_path)

def read_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return f.read()

def search_in_file(file_name: str, search_term: str) -> list:
    results = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if search_term in line:
                results.append((i+1, line.strip()))
    return results

def write_output_file(
    filename: str,
    content: str,
    output_dir: str = "output"
) -> Dict[str, str]:
    """
    Write content to a file inside the output directory.
    Creates the directory if it does not exist.
    """

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "output_path": file_path,
        "bytes_written": len(content.encode("utf-8"))
    }
