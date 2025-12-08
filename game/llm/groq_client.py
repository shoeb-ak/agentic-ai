import json
from groq import Groq
from game.language.prompt import Prompt


class GroqClient:
    """
    Groq LLM wrapper that supports:
    - Standard tool_calls
    - JSON tool calls inside message.content (Llama fallback)
    """

    def __init__(self, api_key=None, model="llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model

    def __call__(self, prompt: Prompt) -> str:
        system = {"role": "system", "content": prompt.system}
        messages = [system] + prompt.messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=prompt.tools,
            tool_choice="auto",
            max_tokens=1024,
        )

        message = response.choices[0].message

        # --------------------------------------------
        # 1. Preferred path: Real Groq tool_calls
        # --------------------------------------------
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            return json.dumps({"tool": tool_name, "args": args})

        # --------------------------------------------
        # 2. Fallback: JSON tool call returned in content
        # (Llama models often do this even with tool_choice="auto")
        # --------------------------------------------
        content = message.content

        try:
            parsed = json.loads(content)
            if "tool" in parsed and "args" in parsed:
                return content  # already valid JSON
        except json.JSONDecodeError:
            pass

        # --------------------------------------------
        # 3. Failure: neither tool_calls nor valid JSON
        # --------------------------------------------
        raise ValueError(
            f"Model returned invalid tool call format:\n"
            f"content={message.content}\n"
            f"tool_calls={message.tool_calls}"
        )
