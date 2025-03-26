from typing import Optional
from app.application.ai_model import AIModel
from app.util.exceptions import ExternalServiceException

import google.generativeai as genai
from app.adapters.repositories.content_repository import ContentRepository
from app.domain.content import Content
from app.util.adapters.ai_api_settings import AIApiSettings
from app.util.ia_api_prompts import PROMPT_GENRE_SYNOPSIS
from app.util.logging.logger import Log


class GenAIModel(AIModel):    
    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        genai.configure(api_key=api_key),
        self.model = self._create_model(model)
                
    def generate_content(self, title) -> Optional[str]:
        try:
            prompt = PROMPT_GENRE_SYNOPSIS.format(title=title)
            response = self.model.generate_content(prompt)
            text = response.text
        except Exception as e:
            Log.logger.error(f"GenAIModel failed obtaining info for title: {title}. Detailed Error: {e}")
            raise ExternalServiceException(f"Cannot get the information for the title: {title}")
        return self._format_text(text)
     
    def _create_model(self, model: str) -> genai.GenerativeModel:
        return genai.GenerativeModel(model)
    
    def _format_text(self, text: str) -> Optional[str]:
        if text and len(text) > 10:
            json_string = text[7:-3]
            return json_string
        else:
            return None
    