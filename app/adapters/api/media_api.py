import json
from fastapi import APIRouter, Depends, Path, Query, status
from dependency_injector.wiring import Provide, inject
from fastapi.responses import JSONResponse


from app.adapters.repositories.channel_repository import ChannelRepository
from app.application.channel_service import ChannelService
from app.application.content_service import ContentService
from app.application.ai_api_service import AIApiService
from app.containers import Container
from app.domain.channel import Channel
from app.util.exceptions import NotFoundException
from app.util.logging.logger import Log


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
    channel = channel_service.get_channel_by_id(channel_id)
    if not channel:
         raise NotFoundException("Channel not found")
    return channel


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
    channels = channel_service.get_first_level_channels()
    if not channels:
        raise NotFoundException("First level Channels not found")
    return channels


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
    channels = channel_service.get_sub_channels(
        channel_id, max_level=MAX_SUBCHANNEL_LEVEL
    )
    if channels is None:
        raise NotFoundException(f"SubChannels for channel {channel_id} not found")
    
    return channels


@router.get(
    path="/content/{content_id}",
    name="Get content info",
)
@inject
async def get_content_by_id(
    content_id: str = Path(..., description="Content Id"),
    content_service: ContentService = Depends(Provide[Container.content_service]),
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Content Not Found"},
    },
):
    content = content_service.get_content_by_id(content_id)
    if not content:
        raise NotFoundException("Content not found")
    return content


@router.get(
    path="/content-suggestions",
    name="Get content suggested info by its title",
)
@inject
async def get_content_suggestion_by_title(
    title: str = Query(..., description="Title of a Movie or TV show"),
    ai_api_service: AIApiService = Depends(Provide[Container.ai_api_service]),
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Title Not Found"},
    },
):
    result = ai_api_service.get_content_suggestion(title)
    
    if not result:
        raise NotFoundException(f"This title cannot be found: {title}")
    
    return result
