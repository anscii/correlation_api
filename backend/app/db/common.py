import os

from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
    database = Database(DB_URL)

    try:
        await database.connect()
        app.state._db = database

    except Exception as err:
        logger.warning("DB CONNECTION ERROR: %s", err)


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()

    except Exception as err:
        logger.warning("DB DISCONNECT ERROR: %s", err)
