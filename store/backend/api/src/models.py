from typing import Optional
import uuid
from pydantic import BaseModel, Field


class ItemModel(BaseModel):
    # Model
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)

    class Config:
        # Workaround to allow underscored variable names
        # If this is not set to True, pydantic will assume it is a private variable
        allow_population_by_field_name = True
        # Schema that will be displayed in auto generated OpenAPI doc
        schema_extra = {
            "example": {
                "name": "My important item",
                "description": "This item is new",
                "price": 5.60,
                "stock": 10,
            }
        }


class UpdateItemModel(BaseModel):
    # Model
    # We do not specify _id field here, because this field is immutable in MongoDB
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]

    class Config:
        # Schema that will be displayed in auto generated OpenAPI doc
        schema_extra = {
            "example": {
                "name": "My important item",
                "description": "This item is new",
                "price": 5.60,
                "stock": 10,
            }
        }
