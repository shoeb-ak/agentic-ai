from game.actions.core.decorators import register_tool

@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminate the conversation with a helpful summary
    Args:
       message: Termination message 
    """
    return message