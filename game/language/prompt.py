class Prompt:
    """
    Simple representation of a full LLM prompt.
    This object is passed to the LLM backend (generate_response).
    """

    def __init__(self, system: str, messages: list, tools: list = None):
        self.system = system
        self.messages = messages  # Past memory
        self.tools = tools or []  # Function-calling schemas

    def to_dict(self):
        """Return the prompt in a structure usable by any LLM SDK."""
        return {
            "system": self.system,
            "messages": self.messages,
            "tools": self.tools
        }

