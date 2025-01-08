from dependency_injector import containers, providers

from app.adapters.repositories.channel_repository import ChannelRepository
from app.adapters.repositories.content_repository import ContentRepository
from app.application.channel_service import ChannelService
from app.application.content_service import ContentService
from app.util.adapters.database_settings import DatabaseSettings

class Container(containers.DeclarativeContainer):
    database_settings = providers.Singleton(DatabaseSettings)
    
    channel_repository_mongo = providers.Singleton(ChannelRepository)
    content_repository_mongo = providers.Singleton(ContentRepository)
    
    content_service = providers.Singleton(
        ContentService,
        content_repository_mongo,
    )
    
    channel_service = providers.Singleton(
        ChannelService,
        content_service,
        channel_repository_mongo,
    )
