from bson import ObjectId
from app.adapters.repositories.channel_db import ChannelDB
from app.domain.channel import Channel


class ChannelMapper():
    def to_domain(self, channel_db: ChannelDB) -> Channel:
        return Channel(
            id=str(channel_db.id),
            title=channel_db.title,
            language=channel_db.language,
            picture=channel_db.picture,
            parents=[
                str(channel) for channel in channel_db.parents
            ] if channel_db.parents else None,
            contents=[
                str(content) for content in channel_db.contents
            ] if channel_db.contents else None,
        )
        
    def to_domain_from_dict(self, channel_db: dict) -> Channel:
        return Channel(
            id=str(channel_db.get("_id")),
            title=channel_db.get("title"),
            language=channel_db.get("language"),
            picture=channel_db.get("picture"),
            parents=[
                str(channel) for channel in channel_db.get("parents")
            ] if channel_db.get("parents") else None,
            contents=[
                str(content) for content in channel_db.get("contents")
            ] if channel_db.get("contents") else None,
        )

    def to_persistence(self, channel: Channel) -> ChannelDB:
        raise NotImplementedError
