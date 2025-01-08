from fastapi import APIRouter, Depends, Path, status
from dependency_injector.wiring import Provide, inject
from fastapi.responses import JSONResponse

from app.adapters.repositories.channel_repository import ChannelRepository
from app.application.channel_service import ChannelService
from app.application.content_service import ContentService
from app.containers import Container
from app.domain.channel import Channel

MAX_SUBCHANNEL_LEVEL = 1

router = APIRouter(
    prefix="/media",
    tags=["Media Platform Management"],
)


@router.get(
    path="/channel/{channel_id}",
    name="Get a channel info",
)
@inject
async def get_channel_by_id(
    channel_id: str = Path(..., description="Channel Id"),
    channel_service: ChannelService = Depends(Provide[Container.channel_service]),
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Channel Not Found"},
    },
):
    try:
        channel = channel_service.get_channel_by_id(channel_id)
        if not channel:
            return _exception("Channel not found 1", status.HTTP_404_NOT_FOUND)
        return channel
    except BaseException as e:
        return _exception(
            f"An error as occurred {e}", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    path="/first_level_channels",
    name="Get first level channels",
)
@inject
async def first_level_channels(
    channel_service: ChannelService = Depends(Provide[Container.channel_service]),
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Channels Not Found"},
    },
):
    try:
        channels = channel_service.get_first_level_channels()
        if not channels:
            return _exception("Channels not found", status.HTTP_404_NOT_FOUND)
        return channels
    except BaseException as e:
        return _exception(
            f" * An error as occurred {e}", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    path="/channel/{channel_id}/channels",
    name="Get sub channels of a channel",
)
@inject
async def get_subchannels(
    channel_id: str = Path(..., description="Channel Id"),
    channel_service: ChannelService = Depends(Provide[Container.channel_service]),
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Channel Not Found"},
    },
):
    try:
        channels = channel_service.get_sub_channels(
            channel_id, max_level=MAX_SUBCHANNEL_LEVEL
        )
        if channels is None:
            return _exception("Channel not found", status.HTTP_404_NOT_FOUND)
        return channels
    except BaseException as e:
        return _exception(
            f"An error as occurred {e}", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    path="/content/{content_id}",
    name="Get content info",
)
@inject
async def get_content_by_id(
    content_id: str = Path(..., description="Content Id"),
    content_service: ContentService = Depends(Provide[Container.content_service]),
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Channel Not Found"},
    },
):
    try:
        content = content_service.get_content_by_id(content_id)
        if not content:
            return _exception("Content not found", status.HTTP_404_NOT_FOUND)
        return content
    except BaseException as e:
        return _exception(
            f"An error as occurred {e}", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _exception(message, code):
    return JSONResponse(
        status_code=code,
        content={"detail": [{"msg": message}]},
    )
