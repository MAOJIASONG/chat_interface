from .openai_api import OpenAIProvider
from .ollama_api import OllamaProvider

PROVIDERS = {
    "OpenAI": OpenAIProvider,
    "Ollama": OllamaProvider,
}

def get_provider(provider_name, model=None, **kwargs):
    """获取指定的 LLM 提供者"""
    try:
        return PROVIDERS[provider_name](model=model, **kwargs)
    except KeyError:
        raise ValueError(f"Unknown provider: {provider_name}")

def list_providers():
    return list(PROVIDERS.keys()) 