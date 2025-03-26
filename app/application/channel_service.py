from operator import itemgetter
from typing import List, Optional

from bson import ObjectId
from app.adapters.repositories.channel_repository import ChannelRepository
from app.application.content_service import ContentService
from app.domain.channel import Channel


class ChannelService:
    def __init__(
        self,
        content_service: ContentService,
        channel_repository: ChannelRepository,
    ):
        self.channel_repository = channel_repository
        self.content_service = content_service

    def get_channel_by_id(self, channel_id: str) -> Optional[Channel]:
        return self.channel_repository.get_channel_by_id(channel_id)

    def get_first_level_channels(self) -> List[Channel]:
        channels = self.channel_repository.get_first_level_channels()
        self._set_contents(channels)
        return channels

    def get_sub_channels(
        self, channel_id: str, max_level: int
    ) -> Optional[List[Channel]]:
        channel = self.channel_repository.get_channel_by_id(channel_id)
        if not channel:
            return None
        channels = self.channel_repository.get_subchannels(channel_id, max_level)
        self._set_contents(channels)
        return channels

    def calculate_ratings(self, csv: dict[str, float] = {}) -> dict:
        first_level_channels = self.channel_repository.get_first_level_channels()
        rating = 0.0
        # Get first level channels, for example movies and lifestyle
        for first_level in first_level_channels:
            print(f"Processing first level channel: {first_level.id}")
            if first_level.contents:
                content_ids = [ObjectId(content) for content in first_level.contents]
                rating = self._calculate_rating(content_ids)
            else:
                # Process only the channels underneath the first level channel
                sub_channels = self.channel_repository.get_subchannels_reduced_fields(
                    first_level.id
                )
                rating = self._get_ratings_from_children(
                    sub_channels, ObjectId(first_level.id), csv
                )

            csv[first_level.title] = rating
            sorted_csv = {k: v for k, v in sorted(csv.items(), key=itemgetter(1), reverse=True)}
        return sorted_csv

    def _get_ratings_from_children(
        self, channels: List[dict], channel_id: ObjectId, csv: dict
    ) -> float:
        children = [
            children
            for children in channels
            if channel_id in children.get("parents")
        ]
        try:
            rating = 0.0
            for child in children:
                # Avoid already rating channel. It could happens when a channel have many parent channels.
                child_rating = 0.0
                if child.get("title") in csv:
                    child_rating = csv.get(child.get("title"))
                elif child.get("contents"):
                    # If contents found, then calculate the average rating of them
                    print(f"Getting content average for channel {child.get('_id')}")
                    content_ids: List[ObjectId] = child.get("contents")
                    child_rating = self._calculate_rating(content_ids)
                else:
                    # Have subchannels, so we need to get ratings from them
                    print(f"Getting rating in  subchannel for {child.get('_id')}")
                    child_rating = self._get_ratings_from_children(
                        channels, child.get("_id"), csv
                    )
                csv[child.get("title")] = child_rating
                rating += child_rating

            return rating / len(children) if children else 0
        except Exception as e:
            raise Exception(
                f" * Exception processing children of channel_id: {channel_id}, children_id: {child.get('_id')}. Detail: {e}\n"
            )


    def _calculate_rating(self, content_ids: List[ObjectId]) -> float:
        contents = self.content_service.get_content_by_list(content_ids)
        rating = sum([content.rating for content in contents]) / len(contents)
        return rating


    def _set_contents(self, channels: Optional[List[Channel]]) -> List[Channel]:
        for channel in channels:
            if channel.contents:
                contents = self.content_service.get_content_by_list(
                    [ObjectId(content) for content in channel.contents]
                )
                rating = sum([content.rating for content in contents]) / len(contents)
                channel.content_data = contents
                channel.rating = rating
        return channels
