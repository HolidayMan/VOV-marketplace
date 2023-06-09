from typing import Optional, ForwardRef

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
    product_data: ProductData

    class Config:
        arbitrary_types_allowed = True


Category = ForwardRef('Category')


class Category(BaseModel):
    id: PositiveInt
    name: str
    parent: Optional[Category] = None


class ProductWithCategories(Product):
    categories: list[Category]
