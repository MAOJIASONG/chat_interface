from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def stream_chat(self, prompt, history):
        pass 