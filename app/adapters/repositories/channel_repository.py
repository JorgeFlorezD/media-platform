from typing import List, Optional, Type

from bson import ObjectId
from app.adapters.repositories.channel_db import ChannelDB
from app.adapters.repositories.channel_mapper import ChannelMapper
from app.adapters.repositories.pipelines import (
    pipeline_subchannel,
    pipeline_subchannel_reduced,
)
from app.domain.channel import Channel
from mongoengine.queryset.visitor import Q


class ChannelRepository:
    @property
    def mapper(self) -> ChannelMapper:
        return ChannelMapper()

    def get_channel_by_id(self, channel_id: str) -> Optional[Channel]:
        document = ChannelDB.objects(id=ObjectId(channel_id)).first()
        return self.mapper.to_domain(document) if document else None

    def get_channel_by_title(self, title: str) -> Optional[Channel]:
        document = ChannelDB.objects(
            title=title,
        ).first()
        return self.mapper.to_domain(document) if document else None

    def get_first_level_channels(self) -> List[Channel]:
        documents = ChannelDB.objects(
            Q(parents__exists=False),
        )
        return [self.mapper.to_domain(document) for document in documents]

    def get_subchannels(
        self, channel_id: str, max_level: int
    ) -> Optional[List[Channel]]:
        pipeline = pipeline_subchannel(
            channel_id, max_level
        )
        documents = list(ChannelDB.objects().aggregate(pipeline))
        if documents:
            return [
                self.mapper.to_domain_from_dict(document)
                for document in documents[0].get("sub_channels")
            ]
        else:
            return None

    def get_subchannels_reduced_fields(
        self, channel_id: str, max_level: int = 1000
    ) -> List[Channel]:
        pipeline = pipeline_subchannel_reduced(channel_id, max_level)
        documents = list(ChannelDB.objects().aggregate(pipeline))

        return documents

    def _sub_channels_pipeline(
        self, channel_id: str, max_level: int, all_fields: bool
    ) -> List[dict]:

        if all_fields:
            return pipeline_subchannel(channel_id, max_level)
        else:
            return pipeline_subchannel_reduced(channel_id, max_level)
