from pydantic import BaseModel

from domain.product import Product
from domain.types import PositiveInt


class CartItem(BaseModel):
    product: Product | None = None
    count: PositiveInt | None = None
    user_id: PositiveInt | None = None
