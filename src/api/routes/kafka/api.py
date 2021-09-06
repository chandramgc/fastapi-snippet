from fastapi import APIRouter

from src.api.routes.kafka import kafka_info
router = APIRouter()

router.include_router(kafka_info.router, prefix="/kafka")