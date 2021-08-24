from fastapi import APIRouter

from src.api.routes.restaurants import restaurants_info
router = APIRouter()

router.include_router(restaurants_info.router, prefix="/restaurant")