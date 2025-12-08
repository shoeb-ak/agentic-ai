class Memory:
    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        """Convert 'type' to 'role' because Groq requires 'role' key."""
        if "type" in memory:
            memory = {"role": memory["type"], "content": memory["content"]}

        self.items.append(memory)

    def get_memories(self, limit=None):
        return self.items[:limit]

