from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.adapters.api import media_api
from app.containers import Container
from app.events import connect_db_client, create_logger_client
from app.util.exception_handlers import external_service_exception_handler, invalid_id_handler, not_controlled_exception_handler, request_validation_exception_handler, validation_error_exception_handler, value_error_handler
from app.util.exceptions import ExternalServiceException, NotControlledException, NotFoundException
from bson.errors import InvalidId

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

    application.add_exception_handler(NotFoundException, external_service_exception_handler)  # type: ignore
    application.add_exception_handler(ExternalServiceException, external_service_exception_handler)  # type: ignore
    application.add_exception_handler(RequestValidationError, request_validation_exception_handler)  # type: ignore
    application.add_exception_handler(ValidationError, validation_error_exception_handler)  # type: ignore
    application.add_exception_handler(ValueError, value_error_handler)  # type: ignore
    application.add_exception_handler(NotControlledException, not_controlled_exception_handler)  # type: ignore
    application.add_exception_handler(InvalidId, invalid_id_handler)  # type: ignore
    
    application.add_event_handler("startup", connect_db_client(application))
    application.add_event_handler("startup", create_logger_client(application))
    
    return application
    
app = create_app()
