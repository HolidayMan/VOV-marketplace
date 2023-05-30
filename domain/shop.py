from pydantic import BaseModel, PositiveInt


class ShopData(BaseModel):
    id: PositiveInt | None
    name: str
    description: str
    approved: bool


class Shop(BaseModel):
    id: PositiveInt
    shop_data: ShopData


