from pydantic import BaseModel, PositiveInt


class ShopData(BaseModel):
    id: PositiveInt | None
    name: str
    description: str
    approved: bool


class Shop(BaseModel):
    id: PositiveInt | None
    shop_data: ShopData


