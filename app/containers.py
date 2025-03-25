from dependency_injector import containers, providers

from app.adapters.repositories.channel_repository import ChannelRepository
from app.adapters.repositories.content_repository import ContentRepository
from app.application.channel_service import ChannelService
from app.application.content_service import ContentService
from app.application.ia_api_service import IAApiService, IAApiService
from app.util.adapters.database_settings import DatabaseSettings
from app.util.adapters.ai_api_settings import AIApiSettings

class Container(containers.DeclarativeContainer):
    database_settings = providers.Singleton(DatabaseSettings)
    ai_api_settings = providers.Singleton(AIApiSettings)
    
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

    ia_info_service = providers.Singleton(
        IAApiService,
        ai_api_settings().api_key,
        ai_api_settings().model,
    )