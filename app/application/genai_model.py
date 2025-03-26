from typing import Optional
from app.application.ai_model import AIModel
from app.util.exceptions import ExternalServiceException
from google.generativeai.types import generation_types

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
                
    async def generate_content(self, title) -> Optional[str]:
        try:
            prompt = PROMPT_GENRE_SYNOPSIS.format(title=title)
            response = self.model.generate_content(prompt)
            text = response.text
        except generation_types.BlockedPromptException as e:
            self._log_exception(f"BlockedPromptError: {e}", title)
        except generation_types.StopCandidateException as e:
            self._log_exception(f"StopCandidateException: {e}", title)
        except generation_types.IncompleteIterationError as e:
            self._log_exception(f"IncompleteIterationError: {e}", title)
        except generation_types.BrokenResponseError as e:
            self._log_exception(f"BrokenResponseError: {e}", title)
        except Exception as e:
            self._log_exception(f"Unexpected exception: {e}", title)
        return self._format_text(text)

    def _create_model(self, model: str) -> genai.GenerativeModel:
        return genai.GenerativeModel(model)
    
    def _format_text(self, text: str) -> Optional[str]:
        if text and len(text) > 10:
            json_string = text[7:-3]
            return json_string
        else:
            return None
    
    def _log_exception(self, message: str, title: str):
        Log.logger.error(message)
        raise ExternalServiceException(f"Cannot get the information for the title: {title}")
