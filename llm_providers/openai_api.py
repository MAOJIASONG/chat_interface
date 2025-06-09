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
        return ["gpt-4.1", "o3", "o4-mini", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"]

    def stream_chat(self, prompt, history):
        messages = []
        for msg in history:
            if msg["role"] in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": prompt})
        response = self.client.responses.create(
            model=self.model,
            tools=[{
                "type": "web_search_preview",
                "search_context_size": self.search_context_size,
                "user_location": {
                    "type": "approximate",
                    "country": "GB",
                    "city": "London",
                    "region": "London",
                }
            }],
            tool_choice={"type": "web_search_preview"} if self.web_search else None,
            input=messages,
            stream=True,
        )
        for event in response:
            if hasattr(event, "type") and "output_text.delta" in event.type:
                yield event.delta