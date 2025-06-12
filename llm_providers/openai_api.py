from .base import LLMProvider
from openai import OpenAI
import streamlit as st

class OpenAIProvider(LLMProvider):
    def __init__(self, model=None, web_search=True, search_context_size="medium"):
        self.model = model or st.secrets.get("OPENAI_MODEL", "gpt-3.5-turbo")
        self.web_search = web_search
        self.search_context_size = search_context_size
        self.client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

    @staticmethod
    def get_available_models():
        # api_key = st.secrets.get("OPENAI_API_KEY", "")
        # try:
        #     if api_key:
        #         client = openai.OpenAI(api_key=api_key)
        #         models = client.models.list()
        #         # 只返回 o 系列和 gpt- 系列模型
        #         available = [m.id for m in models.data if m.id.startswith("gpt-") or m.id.startswith("o")]
        #         # 确保o3在第一位
        #         if "o3" in available:
        #             available.remove("o3")
        #             available.insert(0, "o3")
        #         return available
        # except Exception:
        #     pass
        # 默认模型，o3放在第一位
        return ["gpt-4.1", "gpt-4.1-mini", "o3-pro", "o3", "o4-mini", "gpt-4o"]

    def stream_chat(self, prompt, history):
        messages = []
        for msg in history:
            if msg["role"] in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": prompt})
        # Only add web_search_preview tool if supported by the model
        tools = None
        tool_choice = None
        if self.web_search and not self.model.startswith("o"):
            tools = [{
                "type": "web_search_preview",
                "search_context_size": self.search_context_size,
                "user_location": {
                    "type": "approximate",
                    "country": "GB",
                    "city": "London",
                    "region": "London",
                }
            }]
            tool_choice = {"type": "web_search_preview"}
        response = self.client.responses.create(
            model=self.model,
            tools=tools,
            tool_choice=tool_choice,
            input=messages,
            stream=True,
            reasoning={"summary": "auto"} if self.model.startswith("o") else None,
        )
        for event in response:
            if hasattr(event, "type"):
                if "output_text.delta" in event.type:
                    yield {"type": "output_text", "delta": event.delta}
                elif "reasoning_summary_text.delta" in event.type:
                    yield {"type": "reasoning_summary", "delta": event.delta}