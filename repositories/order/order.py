from datetime import datetime

from pydantic import PositiveInt

from domain.order import OrderItem, Order


class OrderItemWithOrderIdAndCreationDate(OrderItem):
    order_id: PositiveInt
    creation_date: datetime


class OrderWithUserId(Order):
    user_id: PositiveInt
