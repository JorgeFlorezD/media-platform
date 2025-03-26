from typing import Optional
from pydantic import BaseModel


class Content(BaseModel):
    id: str
    rating: float
    file: Optional[str]
    metadata: Optional[str]
