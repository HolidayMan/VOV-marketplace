from typing import List, Optional

from fastapi import Request
from pydantic import PositiveInt


def valid_id(id: str) -> bool:
    if not id or not str.isnumeric(id) or not int(id) >= 1:
        return False
    return True


class OrderItemForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors = {}
        self.product_id: Optional[str] = None
        self.order_id: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.product_id = form.get("product_id")
        self.order_id = form.get("order_id")

    def is_valid(self):
        if not valid_id(self.product_id):
            self.errors["product_id"] = "Product id must be number be bigger than 1"
        if not valid_id(self.order_id):
            self.errors["order_id"] = "Order id must be number be bigger than 1"
        if not self.errors:
            return True
        return False

    def get_product_id(self):
        return PositiveInt(self.product_id)

    def get_order_id(self):
        return PositiveInt(self.order_id)


class DeclineOrderItemForm(OrderItemForm):
    def __init__(self, request: Request):
        super().__init__(request)
        self.refuse_reason: Optional[str] = None

    async def load_data(self):
        await super().load_data()
        form = await self.request.form()
        self.refuse_reason = form.get("refuse_reason")

    def is_valid(self):
        if not self.refuse_reason:
            self.errors["refuse_reason"] = "Refuse reason can't be empty"
        return super().is_valid()

    def get_refuse_reason(self):
        return self.refuse_reason
