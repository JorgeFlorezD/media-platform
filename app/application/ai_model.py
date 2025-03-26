from abc import ABC, abstractmethod
from typing import Optional


class AIModel(ABC):
    '''
    False interface used to inject different AI models (genAI, openAI, etc)
    in the AI service
    '''
    @abstractmethod
    def generate_content(self, prompt: str) -> Optional[str]:
        pass
