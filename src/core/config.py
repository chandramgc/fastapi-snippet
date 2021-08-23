import logging
import sys
import configparser
from typing import List
from loguru import logger
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from src.core.logging import InterceptHandler

API_PREFIX = ""

JWT_TOKEN_PREFIX = "Token"  # noqa: S105
VERSION = "0.0.0"
API_VERSION = "v1"

config = Config("src/resource/dev.env")

# Project confiugration

DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret ,default="secret")
PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# API configuration

API_PREFIX = config("API_PREFIX", default="/api")
API_VERSION = config("API_VERSION", default="v0")

# Logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

# Database configuration

DATABASE_DRIVER = config("DATABASE_DRIVER", default="/api")
DATABASE_USERNAME = config("DATABASE_USERNAME")
DATABASE_PASSWORD_HASH = config("DATABASE_PASSWORD_HASH")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_DB_NAME = config("DATABASE_DB_NAME")
DATABASE_ADDITIONAL_STRING= config("DATABASE_ADDITIONAL_STRING")
DATABASE_URL: DatabaseURL = DATABASE_DRIVER + "://" +  DATABASE_USERNAME + ":" + DATABASE_PASSWORD_HASH + "@" + DATABASE_HOST + "/" + DATABASE_DB_NAME + DATABASE_ADDITIONAL_STRING
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

def get_properties():
    config_properties = configparser.RawConfigParser()
    config_properties.read('src/resource/dev.properties')
    details_dict = dict(config_properties.items('DatabaseSection'))
    print(details_dict)