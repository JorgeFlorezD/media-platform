from typing import List, Optional
from bson import ObjectId
from pydantic_settings import BaseSettings
from pydantic import BaseModel

from app.domain.content import Content

class Channel(BaseModel):
    id: str
    title: str
    language: str
    picture: str
    parents: Optional[List[str]] = None
    contents: Optional[List[str]] = None
    content_data: Optional[List[Content]] = None
    rating: Optional[float] = None
 