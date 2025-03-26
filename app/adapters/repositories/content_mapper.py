from typing import Optional
from bson import ObjectId
from app.adapters.repositories.channel_db import ChannelDB
from app.adapters.repositories.content_db import ContentDB
from app.domain.channel import Channel
from app.domain.content import Content


class ContentMapper():
    def to_domain(self, content_db: ContentDB) -> Content:
        return Content(
            id=str(content_db.id),
            rating=content_db.rating,
            file=content_db.file,
            metadata=content_db.metadata,
        )

    def to_persistence(self, content: Content) -> ContentDB:
        raise NotImplementedError
