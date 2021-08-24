from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
import motor.motor_asyncio
from src.core.config import DATABASE_URL
from src.model.schema.restaurant import RestaurantModel

router = APIRouter()
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client.sample_restaurants 

@router.get(
    "/", response_description="List all restaurant", response_model=List[RestaurantModel]
)
async def list_restaurant():

    students = await db["restaurants"].find().to_list(10)

    return students