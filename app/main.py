from fastapi import FastAPI

from app.adapters.api import media_api
from app.containers import Container
from app.events import connect_db_client

app = FastAPI()

def create_app() -> FastAPI:
    container = Container()
    container.wire(
        modules=[
            media_api,
        ],
    )
    
    application = FastAPI(title="Media Platform Application")

    container.init_resources()
    application.container = container  # type: ignore
    
    application.include_router(media_api.router)
    
    application.add_event_handler("startup", connect_db_client(application))
    
    return application
    
app = create_app()


