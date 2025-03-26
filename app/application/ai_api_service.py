import json
from typing import Optional
from app.adapters.repositories.content_mapper import ContentMapper
from app.application.ai_model import AIModel
from app.domain.content_suggestion import ContentSuggestionsResponse
from app.util.exceptions import ExternalServiceException

import google.generativeai as genai
from app.adapters.repositories.content_repository import ContentRepository
from app.domain.content import Content
from app.util.adapters.ai_api_settings import AIApiSettings
from app.util.ia_api_prompts import PROMPT_GENRE_SYNOPSIS
from app.util.logging.logger import Log


class AIApiService:    
    def __init__(
        self,
        model: AIModel,
    ):
        self.model = model
        
    async def get_content_suggestion(self, title: str):
        text = await self.model.generate_content(title)
        if text:
            return self._create_json(text)
        else:
            return None
    
    def _create_json(self, text: str) -> Optional[dict]:
        try:
            json_data = json.loads(text)
            ContentSuggestionsResponse.model_validate(json_data)
            return json_data
        except json.JSONDecodeError as e:
            Log.logger.error(
                f"JSON Decode Error: {e}. Text: {text}"
            )
            raise ExternalServiceException(f"There is a problem processing the information")
        except Exception as e:
            Log.logger.error(
                f"Unexpected error creating JSON: {e}. Text: {text}"
            )
            raise ExternalServiceException(f"There is a problem processing the information")