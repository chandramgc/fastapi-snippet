from logging import error
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from loguru import logger
from motor import motor_asyncio
from src.model.schema.restaurant import RestaurantModel, UpdateRestaurantModel
from src.core.config import DATABASE_URL
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

router = APIRouter()
client = motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client.sample_restaurants


class RestaurantDbCurd:

    async def get_all_restaurants():
        try:
            restaurants = await db["restaurants"].find().to_list()
            return restaurants
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Please contact administrator.")

    async def create_new_restaurant(restaurant: RestaurantModel):
        try:
            restaurant = jsonable_encoder(restaurant)
            new_restaurant = await db["restaurants"].insert_one(restaurant)
            create_restaurant = await db["restaurants"].find_one({"_id": ObjectId(new_restaurant.inserted_id)})

            if(create_restaurant is not None):
                return new_restaurant.inserted_id

            return None
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Please contact administrator.")

    async def get_restaurant_by_id(id: str):
        try:
            if (restaurant := await db["restaurants"].find_one({"restaurant_id": id})) is not None:
                return restaurant
            return None
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Please contact administrator.")

    async def update_restaurant_by_id(id: str, restauant: UpdateRestaurantModel):
        try:
            restauant = {k: v for k, v in restauant.dict().items()
                        if v is not None}
            if len(restauant) > 0:
                update_result = await db["restaurants"].update_one({"restaurant_id": id}, {"$set": restauant})
                print(restauant)
                print(update_result)

                if update_result.modified_count == 1:
                    if (
                        updated_restaurant := await db["restaurants"].find_one({"restaurant_id": id})
                    ) is not None:
                        return True

            if (existing_restaurant := await db["restaurants"].find_one({"restaurant_id": id})) is not None:
                return True

            return False
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Please contact administrator.")

    async def delete_restaurant_by_restaurant_id(id: str):
        try:
            delete_result = await db["restaurants"].delete_one({"restaurant_id": id})
            if delete_result.deleted_count == 1:
                return True

            return False
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Please contact administrator.")
