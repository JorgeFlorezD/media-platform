# from app.adapters.repositories.channel_repository import ChannelRepository
from typing import List, Optional

from bson import ObjectId
from app.adapters.repositories.content_repository import ContentRepository
from app.domain.content import Content


class ContentService:
    def __init__(
        self,
        content_repository: ContentRepository,
    ):
        self.content_repository = content_repository

    def get_content_by_id(self, content_id: str) -> Optional[Content]:
        return self.content_repository.get_content_by_id(content_id)
    
    def get_content_by_list(self, content_ids: List[ObjectId]) -> Optional[List[Content]]:
        return self.content_repository.get_content_by_list(content_ids)
    