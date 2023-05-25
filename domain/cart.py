from pydantic import BaseModel

from domain.product import Product
from domain.types import PositiveInt


class CartItem(BaseModel):
    product: Product
    count: PositiveInt
    user_id: PositiveInt
