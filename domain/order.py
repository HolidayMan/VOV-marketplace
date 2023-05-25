from money import Money
from pydantic import BaseModel
from datetime import datetime
from domain.product import Product
from domain.types import PositiveInt


class OrderItemStatus(BaseModel):
    id: PositiveInt | None = None,
    name: str | None = None


class OrderItem(BaseModel):
    refuse_reason: str | None = None
    product: Product | None = None
    price: Money | None = None
    creation_date: datetime | None = None
    check_date: datetime | None = None
    status: OrderItemStatus | None = None
    count: PositiveInt | None = None

    class Config:
        arbitrary_types_allowed = True


class OrderStatus(BaseModel):
    id: PositiveInt | None = None
    name: str | None = None


class Order(BaseModel):
    user_id: PositiveInt | None = None
    id: PositiveInt | None = None
    order_items: list[OrderItem] | None = None
    status: OrderStatus | None = None





