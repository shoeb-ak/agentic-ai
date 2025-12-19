from game.llm.model_registry import MODEL_REGISTRY
from game.config.config import CONFIG

# Best → worst for tool calling
GROQ_TOOL_PREFERENCE = [
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.1-8b-instant",
    "qwen/qwen3-32b",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
]

class ModelRouter:

    @staticmethod
    def select_model() -> str:
        for model_name in GROQ_TOOL_PREFERENCE:
            if ModelRouter._is_available(model_name):
                return model_name

        raise RuntimeError("No suitable Groq model available")

    @staticmethod
    def _is_available(model_name: str) -> bool:
        # later: rate limits, outages, quotas
        return True