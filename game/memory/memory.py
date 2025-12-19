import json


class Memory:
    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        """
        Enforce LLM-compatible memory format.
        All message content MUST be a string.
        """
        if "content" in memory and not isinstance(memory["content"], str):
            memory = memory.copy()
            memory["content"] = json.dumps(memory["content"])

        self.items.append(memory)

    def get_memories(self, limit=None):
        return self.items[:limit]
