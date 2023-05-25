from decimal import *

from pydantic import BaseModel
from domain.types import PositiveInt
from money import Money


class ProductData(BaseModel):
    id: PositiveInt | None = None
    name: str | None = None
    description: str | None = None
    image_file_path: str | None = None
    approved: bool | None = None


class Product(BaseModel):
    id: PositiveInt | None = None
    price: Money | None = None
    shop_id: PositiveInt | None = None
    product_data: ProductData | None = None

    class Config:
        arbitrary_types_allowed = True


class Category(BaseModel):
    id: PositiveInt | None = None
    name: str | None = None

