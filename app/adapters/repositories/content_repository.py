from typing import List, Optional, Type

from bson import ObjectId
from app.adapters.repositories.channel_db import ChannelDB
from app.adapters.repositories.channel_mapper import ChannelMapper
from app.adapters.repositories.content_db import ContentDB
from app.adapters.repositories.content_mapper import ContentMapper
from app.domain.channel import Channel
from mongoengine.queryset.visitor import Q

from app.domain.content import Content


class ContentRepository: 
    @property
    def mapper(self) -> ContentMapper:
        return ContentMapper()
        
    def get_content_by_id(self, content_id: str) -> Optional[Content]:
        document = ContentDB.objects(id=ObjectId(content_id)).first()            
        return self.mapper.to_domain(document) if document else None
    
    def get_content_by_list(self, content_ids: List[ObjectId]) -> Optional[List[Content]]:
        documents = ContentDB.objects(id__in=content_ids)            
        return [self.mapper.to_domain(document) for document in documents]
    