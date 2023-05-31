from money import Money
from pydantic import BaseModel
from datetime import datetime
from domain.product import Product
from pydantic.types import PositiveInt
from enum import Enum


class OrderItemStatus(Enum):
    IN_PROCESS = "in_process"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    CANCELED = "canceled"


class OrderItem(BaseModel):
    refuse_reason: str | None = None
    product: Product
    # price field stores the price of a single product item at the moment of ordering
    price: Money
    check_date: datetime | None = None
    status: OrderItemStatus
    count: PositiveInt

    class Config:
        arbitrary_types_allowed = True

    def total(self) -> Money:
        return self.price * self.count


class OrderStatus(Enum):
    IN_PROCESS = "in_process"
    CLOSED = "closed"
    CANCELED = "canceled"


class Order(BaseModel):
    user_id: PositiveInt
    id: PositiveInt | None
    order_items: list[OrderItem]
    status: OrderStatus
    creation_date: datetime

    def total(self) -> Money:
        total_cost = Money(0, "UAH")
        for item in self.order_items:
            total_cost += item.total()
        return total_cost





