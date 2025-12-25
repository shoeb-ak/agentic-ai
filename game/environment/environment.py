import traceback

class Environment:
    def execute_action(self, func, args):
        """
        Execute a tool function safely.
        """
        try:
            result = func(**args)
            return {
                "tool_executed": True,
                "result": result,
            }
        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
