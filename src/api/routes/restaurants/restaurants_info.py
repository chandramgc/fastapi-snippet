import json
from typing import List
from bson import json_util
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from src.model.schema.restaurant import RestaurantModel, UpdateRestaurantModel
from src.db.curd.restaurant import RestaurantDbCurd
from starlette.responses import JSONResponse
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                              HTTP_404_NOT_FOUND,
                              HTTP_422_UNPROCESSABLE_ENTITY)

router = APIRouter()


@router.get(
    "/",
    response_description="List all restaurant",
    response_model=List[RestaurantModel]
)
async def list_restaurant():
    restaurants = await RestaurantDbCurd.get_all_restaurants()

    if (restaurants is not None):
        return JSONResponse(status_code=HTTP_200_OK, content=json.loads(json_util.dumps((restaurants))))

    raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail=f"Restaurant {id} not found")


@router.post(
    "/",
    response_model=RestaurantModel,
    status_code=HTTP_201_CREATED,
)
async def create_restaurant(
        restaurant: RestaurantModel = Body(..., embed=True)
):
    _id = await RestaurantDbCurd.create_new_restaurant(restaurant)

    if _id is not None:
        return JSONResponse(status_code=HTTP_201_CREATED, content={"message": f"Restaurant {_id} sccessfully created"})

    raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Restaurant is failed to ineserted.")


@router.get(
    "/{id}",
    response_description="Get single restaurant by id",
    response_model=RestaurantModel
)
async def show_restaurant(id: str):
    restaurant = await RestaurantDbCurd.get_restaurant_by_id(id)

    if restaurant is not None:
        return JSONResponse(status_code=HTTP_200_OK, content=json.loads(json_util.dumps((restaurant))))

    raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail=f"Restaurant {id} not found")


@router.put(
    "/{id}",
    response_description="Upadate single restaurant by id",
    response_model=RestaurantModel
)
async def update_restaurant(
    id: str,
    restauant: UpdateRestaurantModel = Body(...)
):
    result: bool = await RestaurantDbCurd.update_restaurant_by_id(id, restauant)

    if result == True:
        return JSONResponse(status_code=HTTP_200_OK, content={"message": f"Restaurant {id} sccessfully updated"})

    raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail=f"Restaurant {id} not found")


@router.delete(
    "/{id}",
    response_description="Delete single restaurant by id"
)
async def delete_restaurant(id: str):
    result: bool = await RestaurantDbCurd.delete_restaurant_by_restaurant_id(id)

    if result == True:
        return JSONResponse(status_code=HTTP_200_OK, content={"message": f"Restaurant {id} sccessfully deleted"})

    raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail=f"Restaurant {id} not found.")
