from pydantic import Field
from pydantic_settings import BaseSettings

class LoggingSettings(BaseSettings):
    log_level: str = Field(default="DEBUG")
