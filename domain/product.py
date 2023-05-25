from decimal import *

from pydantic import BaseModel
from domain.types import ID
from money import Money


class ProductData(BaseModel):
    id: ID | None = None
    name: str | None = None
    description: str | None = None
    image_file_path: str | None = None
    approved: bool | None = None


class Product(BaseModel):
    id: ID | None = None
    price: Decimal | None = None
    shop_id: ID | None = None
    product_data: ProductData | None = None


class Category(BaseModel):
    id: ID | None = None
    name: str | None = None

