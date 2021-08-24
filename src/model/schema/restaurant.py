from typing import List
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, EmailStr

from src.model.domain.common import DateTimeModelMixin, IDModelMixin, PyObjectId
from src.model.domain.ormmodel import ORMModel


class RestaurantModel(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    restaurant_id: str = Field(...)
    name: str = Field(...)
    cuisine: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "restaurant_id": "40356018",
                "name": "Riviera Caterer",
                "cuisine": "American"
            }
        }

"""
class Restaurant(IDModelMixin, DateTimeModelMixin, ORMModel):
    restaurant_id: str
    name: str
    cuisine: str
"""