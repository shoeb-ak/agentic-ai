from game.llm.groq_client import GroqClient
from game.llm.portkey_client import PortkeyClient
from game.config.config import CONFIG


class LLMFactory:

    @staticmethod
    def create():
        provider = CONFIG.llm.provider.lower()

        if provider == "groq":
            return GroqClient()

        if provider == "portkey":
            return PortkeyClient()

        raise ValueError(f"Unsupported LLM provider: {provider}")
