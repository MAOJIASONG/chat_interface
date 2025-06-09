from .base import LLMProvider
import httpx
import streamlit as st

class OllamaProvider(LLMProvider):
    def __init__(self, model=None):
        self.base_url = st.secrets.get("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or st.secrets.get("OLLAMA_MODEL", "llama3")

    @staticmethod
    def get_available_models():
        base_url = st.secrets.get("OLLAMA_BASE_URL", "http://localhost:11434")
        try:
            resp = httpx.get(f"{base_url}/api/tags", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            pass
        # 默认模型
        return ["llama3", "llama2", "mistral", "qwen:7b", "qwen:14b"]

    def stream_chat(self, prompt, history):
        url = f"{self.base_url}/api/chat"
        messages = []
        for msg in history:
            if msg["role"] in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": prompt})
        payload = {"model": self.model, "messages": messages, "stream": True}
        with httpx.stream("POST", url, json=payload, timeout=60) as response:
            for line in response.iter_lines():
                if line:
                    try:
                        import json
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
                    except Exception:
                        continue 