from typing import Optional

from pydantic import BaseModel
from pydantic.types import PositiveInt
from money import Money

from domain.shop import Shop


class ProductData(BaseModel):
    id: PositiveInt | None
    name: str
    description: str
    image_file_path: str | None = None
    approved: bool


class Product(BaseModel):
    id: PositiveInt | None
    price: Money
    shop: Shop
    product_data: ProductData

    class Config:
        arbitrary_types_allowed = True


class ProductWithCategories(Product):
    categories: list['Category']


class Category(BaseModel):
    id: PositiveInt
    name: str
    parent: Optional['Category'] = None
