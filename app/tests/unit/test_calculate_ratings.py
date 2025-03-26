import os
import sys
from bson import ObjectId
import pytest
from pytest_mock import MockerFixture

from app.adapters.repositories.content_repository import ContentRepository
from app.application.content_service import ContentService
from app.domain.channel import Channel
from app.domain.content import Content

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from app.adapters.repositories.channel_repository import ChannelRepository
from app.application.channel_service import ChannelService


class TestCalculateRatings:
    def test_calculate_rating_in_tree_success(self, mocker: MockerFixture):
        expected_result = {
            "title a5": 8.0,
            "title a3": 6.5,
            "title a1": 5.75,
            "title a4": 5.0,
            "title a2": 5.0,
        }

        first_level_channels = self._initial_channels()
        mocker.patch(
            f"{ChannelRepository.__module__}.{ChannelRepository.get_first_level_channels.__qualname__}",
            return_value=first_level_channels,
        )
        mocker.patch(
            f"{ChannelRepository.__module__}.{ChannelRepository.get_subchannels_reduced_fields.__qualname__}",
            return_value=self._channel_model(),
        )
        channel_service = self._channel_service()
        csv = self._initial_csv()

        ratings = channel_service.calculate_ratings(csv)

        assert ratings == expected_result

    def test_calculate_ratings_from_contents_success(self, mocker: MockerFixture):
        input_ids = [
            ObjectId("0000000000000000000000b1"),
            ObjectId("0000000000000000000000b2"),
            ObjectId("0000000000000000000000b3"),
        ]
        mocker.patch(
            f"{ContentRepository.__module__}.{ContentRepository.get_content_by_list.__qualname__}",
            return_value=self._content_model(),
        )
        channel_service = self._channel_service()

        rating = channel_service._calculate_rating(input_ids)
        
        assert rating == 6

    def _content_service(self):
        return ContentService(
            content_repository=ContentRepository(),
        )

    def _channel_service(self):
        return ChannelService(
            content_service=self._content_service(),
            channel_repository=ChannelRepository(),
        )

    def _initial_channels(self):
        return [
            Channel(
                **{
                    "id": "0000000000000000000000a1",
                    "title": "title a1",
                    "language": "en",
                    "picture": "",
                }
            )
        ]

    def _channel_model(self):
        return [
            {
                "_id": ObjectId("0000000000000000000000a3"),
                "title": "title a3",
                "parents": [ObjectId("0000000000000000000000a1")],
            },
            {
                "_id": ObjectId("0000000000000000000000a4"),
                "title": "title a4",
                "parents": [
                    ObjectId("0000000000000000000000a2"),
                    ObjectId("0000000000000000000000a3"),
                ],
                "contents": [
                    ObjectId("0000000000000000000000b1"),
                    ObjectId("0000000000000000000000b2"),
                ],
            },
            {
                "_id": ObjectId("0000000000000000000000a5"),
                "title": "title a5",
                "parents": [ObjectId("0000000000000000000000a3")],
                "contents": ["0000000000000000000000b3"],
            },
            {
                "_id": ObjectId("0000000000000000000000a2"),
                "title": "title a2",
                "parents": [ObjectId("0000000000000000000000a1")],
            },
        ]

    def _initial_csv(self):
        return {"title a4": 5.0, "title a5": 8.0}

    def _content_model(self):
       return [
            Content(
                **{
                    "id": "0000000000000000000000b1",
                    "file": "file 1",
                    "metadata": "{}}",
                    "rating": 4,
                    "parent_id": "0000000000000000000000a3",
                }
            ),
            Content(
                **{
                    "id": "0000000000000000000000b2",
                    "file": "file 2",
                    "metadata": "{}}",
                    "rating": 6,
                    "parent_id": "0000000000000000000000a3",
                }
            ),
            Content(
                **{
                    "id": "0000000000000000000000b3",
                    "file": "file 3",
                    "metadata": "{}",
                    "rating": 8,
                    "parent_id": "0000000000000000000000b2",
                },
            ),
        ]
