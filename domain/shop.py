from pydantic import BaseModel, PositiveInt


class ShopData(BaseModel):
    id: PositiveInt | None
    name: str
    description: str
    approved: bool


class Shop(BaseModel):
    shop_data: ShopData


