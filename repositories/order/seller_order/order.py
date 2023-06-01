from datetime import datetime

from pydantic import PositiveInt

from domain.order import OrderItem


class OrderItemWithOrderIdAndCreationDate(OrderItem):
    order_id: PositiveInt
    creation_date: datetime
