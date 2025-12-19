from typing import Callable, Dict

from .file_agent.agent import create_agent as create_file_agent
from .readme_agent.agent import create_agent as create_readme_agent


class AgentFactory:
    """
    Central registry for creating agents.
    """

    _registry: Dict[str, Callable] = {
        "file": create_file_agent,
        "readme": create_readme_agent,
    }

    @classmethod
    def create(cls, agent_type: str):
        if agent_type not in cls._registry:
            raise ValueError(
                f"Unknown agent type '{agent_type}'. "
                f"Available agents: {list(cls._registry.keys())}"
            )

        return cls._registry[agent_type]()
