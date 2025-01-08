from typing import Optional

# old: from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    mongo_db_name: str = "platform"
    mongo_db_host: str = "127.0.0.1"
    mongo_db_port: int = 27017
    mongo_db_user: Optional[str] = ""
    mongo_db_password: Optional[str] = ""
