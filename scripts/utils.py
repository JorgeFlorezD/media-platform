from datetime import datetime, timezone
import os
from mongoengine import connect, disconnect
from datetime import datetime


def generate_utc_timestamp() -> str:
    return str(datetime.now().timestamp())


def connect_database():
    connect(**_get_db_connection_details())
    print("Connected to database\n")


def disconnect_database():
    print("Disconnected from database\n")
    disconnect()


def _get_db_connection_details():
    if "MONGO_DB_USER" in os.environ and "MONGO_DB_PASSWORD" in os.environ:
        db_connection_details = {
            "db": os.environ["MONGO_DB_NAME"],
            "host": os.environ["MONGO_DB_HOST"],
            "port": os.environ["MONGO_DB_PORT"],
            "username": os.environ["MONGO_DB_USER"],
            "password": os.environ["MONGO_DB_PASSWORD"],
        }
    else:
        db_connection_details = {
            "db": os.environ["MONGO_DB_NAME"],
            "host": os.environ["MONGO_DB_HOST"],
            "port": int(os.environ["MONGO_DB_PORT"]),
        }

    return db_connection_details
