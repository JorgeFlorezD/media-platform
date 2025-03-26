from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from bson.errors import InvalidId

from app.util.exceptions import ExternalServiceException, NotControlledException, NotFoundException

async def not_found_exception_handler(request: Request, exception: NotFoundException):
    return JSONResponse(
        status_code=exception.code,
        content={"detail": exception.message, "code": exception.code},
    )

async def not_controlled_exception_handler(request: Request, exception: NotControlledException):
    return JSONResponse(
        status_code=exception.code,
        content={"detail": exception.message, "code": exception.code},
    )

async def external_service_exception_handler(request: Request, exception: ExternalServiceException):
    return JSONResponse(
        status_code=exception.code,
        content={"detail": exception.message, "code": exception.code},
    )

async def validation_error_exception_handler(request: Request, exception: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": jsonable_encoder(exception.errors())},
    )

async def request_validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": jsonable_encoder(exception.errors())},
    )

async def value_error_handler(request: Request, error: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": error.args[0]},
    )
    
async def invalid_id_handler(request: Request, error: InvalidId):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": error.args[0]},
    )
