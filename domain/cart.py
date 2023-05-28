from money import Money
from pydantic import BaseModel

from domain.product import Product
from pydantic.types import PositiveInt


class CartItem(BaseModel):
    product: Product
    count: PositiveInt
    user_id: PositiveInt | None

    def total(self) -> Money:
        product_price = self.product.price
        return product_price * self.count
