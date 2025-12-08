import json

class FunctionCallParser:
    """
    Parses JSON-based function calls from LLM responses.
    Expected format:
    {
        "tool": "read_file",
        "args": {"file_name": "hello.txt"}
    }
    """

    @staticmethod
    def parse(response_text: str):
        """
        Parse the JSON function call returned by the LLM.
        LLM MUST return valid JSON (enforced in the system prompt).
        """
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON returned by LLM: {response_text}")

        if "tool" not in data or "args" not in data:
            raise ValueError(
                f"Response missing required fields ('tool', 'args'): {response_text}"
            )

        return {
            "tool": data["tool"],
            "args": data["args"]
        }

