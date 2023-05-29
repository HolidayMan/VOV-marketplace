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


class OrderItem(BaseModel):
    refuse_reason: str | None = None
    product: Product
    price: Money
    creation_date: datetime
    check_date: datetime | None = None
    status: OrderItemStatus
    count: PositiveInt

    class Config:
        arbitrary_types_allowed = True


class OrderStatus(Enum):
    IN_PROCESS = "in_process"
    CLOSED = "closed"
    CANCELED = "canceled"


class Order(BaseModel):
    user_id: PositiveInt
    id: PositiveInt
    order_items: list[OrderItem]
    status: OrderStatus





