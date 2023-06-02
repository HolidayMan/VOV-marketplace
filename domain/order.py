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

    def can_be_processed(self) -> bool:
        return self.status == OrderItemStatus.IN_PROCESS


class OrderStatus(Enum):
    IN_PROCESS = "in_process"
    CLOSED = "closed"
    CANCELED = "canceled"


class Order(BaseModel):
    id: PositiveInt | None
    order_items: list[OrderItem]
    status: OrderStatus
    creation_date: datetime

    def total(self) -> Money:
        total_cost = Money(0, "UAH")
        for item in self.order_items:
            total_cost += item.total()
        return total_cost

    def can_be_canceled(self) -> bool:
        # if at least one item is already accepted by seller, the order can't be canceled
        # if order is already canceled than it can't be canceled
        if self.status == OrderStatus.CANCELED:
            return False
        for item in self.order_items:
            if item.status == OrderItemStatus.ACCEPTED:
                return False
        return True





