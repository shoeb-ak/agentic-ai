from abc import ABC, abstractmethod
from game.language.prompt import Prompt

class BaseLLMClient(ABC):

    @abstractmethod
    def __call__(self, prompt: Prompt) -> dict:
        """
        Must return:
        {
            "tool": "<tool_name>",
            "args": {...}
        }
        """
        pass
