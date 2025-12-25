from game.actions.core.actions_registry import get_tools_by_tags


class ActionRegistry:
    """
    Agent-scoped view of allowed tools.
    """

    def __init__(self, tags=None):
        self._tools = get_tools_by_tags(tags)

    def list_tools(self):
        return self._tools.values()

    def get_tool(self, name):
        return self._tools[name]

    def get_openai_schema(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["tool_name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"],
                },
            }
            for tool in self._tools.values()
        ]

