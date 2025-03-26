from typing import Callable
from fastapi import FastAPI
from mongoengine import connect, disconnect  # type: ignore
from structlog.contextvars import bind_contextvars

from app.util.adapters.database_settings import DatabaseSettings
from app.util.logging.logger import Log

def connect_db_client(app: FastAPI) -> Callable:
    async def execute():
        try:
            db_settings: DatabaseSettings = app.container.database_settings()
            connect(**__get_db_connection_details(db_settings))
        except Exception as e:
            return(f" Exception connecting to database")

    return execute

def create_logger_client(app: FastAPI) -> Callable:
    async def execute():
        logging_settings = app.container.logging_settings()
        Log.setup_logging(logging_settings.log_level, app.title)
        bind_contextvars(component="SERVER")
        Log.logger.debug("Initializing logging ...")

    return execute

def __get_db_connection_details(db_settings):
    if db_settings.mongo_db_user and db_settings.mongo_db_password:
        db_connection_details = {
            "db": db_settings.mongo_db_name,
            "host": db_settings.mongo_db_host,
            "port": db_settings.mongo_db_port,
            "username": db_settings.mongo_db_user,
            "password": db_settings.mongo_db_password,
        }
    else:
        db_connection_details = {
            "db": "platform",
            "host": "localhost",
            "port": 27017,
        }
        # db_connection_details = {
        #     "db": db_settings.mongo_db_name,
        #     "host": db_settings.mongo_db_host,
        #     "port": db_settings.mongo_db_port,
        # }

    return db_connection_details