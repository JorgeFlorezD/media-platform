from typing import Optional

from pydantic_settings import BaseSettings


class AIApiSettings(BaseSettings):
    api_key: str = "test"
    model: str = "gemini-2.0-flash"
