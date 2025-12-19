import json
from groq import Groq
from game.language.prompt import Prompt
from game.config.config import CONFIG
from game.llm.model_router import ModelRouter


class GroqClient:
    """
    Groq-native LLM wrapper.

    Contract:
    - Uses ONLY Groq tool_calls
    - Enforces exactly one tool call
    - Never parses JSON from message.content
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ):
        self.client = Groq(api_key=api_key)

        self.model = model or ModelRouter.select_model()
        self.max_tokens = max_tokens or CONFIG.llm.max_tokens
        self.temperature = temperature or CONFIG.llm.temperature

        print(f"[LLM] Provider=Groq | Model={self.model}")

    def __call__(self, prompt: Prompt) -> dict:
        system = {"role": "system", "content": prompt.system}
        messages = [system] + prompt.messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=prompt.tools,
            tool_choice="required",
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        message = response.choices[0].message

        # --------------------------------------------
        # ONLY VALID PATH: Groq-native tool_calls
        # --------------------------------------------
        if not message.tool_calls:
            # Model violated contract → force terminate
            return {
                "tool": "terminate",
                "args": {
                    "message": "Model failed to call a tool. Terminating safely."
                }
            }

        # Enforce exactly one tool call
        tool_call = message.tool_calls[0]

        return {
            "tool": tool_call.function.name,
            "args": json.loads(tool_call.function.arguments),
        }

