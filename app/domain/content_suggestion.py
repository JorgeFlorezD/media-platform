from pydantic import BaseModel, RootModel
from typing import List

class ContentSuggestion(BaseModel):
    title: str
    synopsis: str
    genres: List[str]
    
class ContentSuggestionsResponse(RootModel[List[ContentSuggestion]]):
    pass