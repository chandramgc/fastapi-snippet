import logging
import sys
from typing import List

from loguru import logger
from src.core.logging import InterceptHandler
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

JWT_TOKEN_PREFIX = "Token"  # noqa: S105
VERSION = "0.0.0"

config = Config("src/resource/dev_mongo.env")

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

# Kafka configuration

KAFKA_BOOTSTRAP_HOST_NAME = config("KAFKA_BOOTSTRAP_HOST_NAME", default="localhost")
KAFKA_BOOTSTRAP_PORT_NUMBER = config("KAFKA_BOOTSTRAP_PORT_NUMBER", default="9092")
KAFKA_CLIENT = KAFKA_BOOTSTRAP_HOST_NAME + ":" + KAFKA_BOOTSTRAP_PORT_NUMBER
ZOOKEEPER_HOST_NAME = config("ZOOKEEPER_HOST_NAME", default="localhost")
ZOOKEEPER_PORT_NUMBER = config("ZOOKEEPER_PORT_NUMBER", default="2181")
ZOOKEEPER_CLIENT = ZOOKEEPER_HOST_NAME + ":" + ZOOKEEPER_PORT_NUMBER
KAFKA_TOPIC = config("KAFKA_TOPIC", default="test")

