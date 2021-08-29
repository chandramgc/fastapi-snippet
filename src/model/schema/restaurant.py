from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from src.model.domain.common import PyObjectId


class GradeModel(BaseModel):
    date: datetime = Field(...)
    grade: str = Field(...)
    score: int = Field(...)


class AddressModel(BaseModel):
    building: str = Field(...)
    street: str = Field(...)
    zipcode: str = Field(...)
    coord: List[float] = Field(...)


class RestaurantId(BaseModel):
    _id: PyObjectId = None


class RestaurantModel(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    restaurant_id: str = Field(...)
    name: str = Field(...)
    cuisine: str = Field(...)
    borough: str = Field(...)
    address: AddressModel = Field(...)
    grades: List[GradeModel] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: lambda x: ObjectId(x)}
        schema_extra = {
            "example": {
                "_id": "ObjectId('5eb3d668b31de5d588f4292a')",
                "restaurant_id": "40356018",
                "name": "Riviera Caterer",
                "cuisine": "American",
                "borough": "Brooklyn",
                "address": {
                    "building": "2780",
                    "street": "Stillwell Avenue",
                    "zipcode": "11224",
                    "coord": [
                        -73.98241999999999,
                        40.579505
                    ]
                },
                "grades": [
                    {
                        "date": "2014-06-10T00:00:00.000+00:00",
                        "grade": "A",
                        "score": 5
                    },
                    {
                        "date": "2013-06-05T00:00:00.000+00:00",
                        "grade": "A",
                        "score": 7
                    },
                    {
                        "date": "2012-04-13T00:00:00.000+00:00",
                        "grade": "A",
                        "score": 12
                    }
                ]
            }
        }


class UpdateRestaurantModel(BaseModel):
    restaurant_id: Optional[str]
    name: Optional[str]
    cuisine: Optional[str]
    borough: Optional[str]
    address: Optional[AddressModel]
    grades: Optional[List[GradeModel]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "restaurant_id": "40356018",
                "name": "Riviera Caterer",
                "cuisine": "American",
                "borough": "Brooklyn",
                "address": {
                    "building": "2780",
                    "street": "Stillwell Avenue",
                    "zipcode": "11224",
                    "coord": [
                        -73.98241999999999,
                        40.579505
                    ]
                },
                "grades": [
                    {
                        "date": "2014-06-10T00:00:00.000+00:00",
                        "grade": "A",
                        "score": 5
                    },
                    {
                        "date": "2013-06-05T00:00:00.000+00:00",
                        "grade": "A",
                        "score": 7
                    },
                    {
                        "date": "2012-04-13T00:00:00.000+00:00",
                        "grade": "A",
                        "score": 12
                    }
                ]
            }
        }