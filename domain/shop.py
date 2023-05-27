from pydantic import BaseModel
from domain.types import PositiveInt


class ShopData(BaseModel):
    id: PositiveInt
    name: str
    description: str
    approved: bool


class Shop(BaseModel):
    id: PositiveInt
    shop_data: ShopData


