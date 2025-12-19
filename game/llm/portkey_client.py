import json
from portkey_ai import Portkey
from game.llm.base_client import BaseLLMClient
from game.language.prompt import Prompt
from game.config.config import CONFIG


class PortkeyClient(BaseLLMClient):
    """
    Portkey-backed LLM client.
    Safer for agents because Portkey normalizes tool calling.
    """
    MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: str | None = None,
        virtual_key: str | None = None,
        model: str | None = None,
    ):
        self.client = Portkey(
            api_key=api_key or CONFIG.portkey.api_key,
            virtual_key=virtual_key or CONFIG.portkey.virtual_key,
        )

        #self.model = model or CONFIG.llm.model

        print(f"[LLM] Provider=Portkey | Model={self.MODEL}")

    def __call__(self, prompt: Prompt) -> dict:
        system = {"role": "system", "content": prompt.system}
        messages = [system] + prompt.messages

        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            tools=prompt.tools,
            tool_choice="required",   # Portkey handles enforcement
            max_tokens=CONFIG.llm.max_tokens,
            temperature=CONFIG.llm.temperature,
        )

        message = response.choices[0].message

        # Portkey normalizes tool calls well
        if not message.tool_calls:
            return {
                "tool": "terminate",
                "args": {"message": "Model failed to call a tool"}
            }

        tool_call = message.tool_calls[0]
        return {
            "tool": tool_call.function.name,
            "args": json.loads(tool_call.function.arguments),
        }
