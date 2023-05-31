from money import Money
from pydantic import BaseModel

from domain.product import Product
from pydantic.types import PositiveInt


class CartItem(BaseModel):
    product: Product
    count: PositiveInt
    user_id: PositiveInt | None
    # price field stores the price of a single product item at the moment of ordering
    price: Money | None

    class Config:
        arbitrary_types_allowed = True

    def total(self) -> Money:

        return self.product.price * self.count
