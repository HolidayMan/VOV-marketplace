from decimal import *

from pydantic import BaseModel
from pydantic.types import PositiveInt
from money import Money


class ProductData(BaseModel):
    id: PositiveInt
    name: str
    description: str
    image_file_path: str | None = None
    approved: bool


class Product(BaseModel):
    id: PositiveInt
    price: Money
    shop_id: PositiveInt
    product_data: ProductData

    class Config:
        arbitrary_types_allowed = True


class Category(BaseModel):
    id: PositiveInt
    name: str

