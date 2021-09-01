import configparser
import logging
import sys
from typing import List

from databases import DatabaseURL
from loguru import logger
from src.core.logging import InterceptHandler
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

JWT_TOKEN_PREFIX = "Token"  # noqa: S105
VERSION = "0.0.0"

config = Config("src/resource/dev.env")

# Project confiugration

DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="secret")
PROJECT_NAME: str = config(
    "PROJECT_NAME", default="FastAPI example application")
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