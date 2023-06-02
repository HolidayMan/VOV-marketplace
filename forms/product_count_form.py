from typing import List, Optional

from fastapi import Request
from pydantic import PositiveInt


class ProductCountForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.count: Optional[str] = None
        self.product_id: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.count = form.get("count")
        self.product_id = form.get("product_id")

    async def is_valid(self):
        if not self.count or not str.isnumeric(self.count) or not (int(self.count) >= 1):
            self.errors.append("Count must be number more than 1")
        if not self.product_id or not str.isnumeric(self.product_id) or not (int(self.product_id) >= 1):
            self.errors.append("Invalid product id")
        if not self.errors:
            return True
        return False

    async def get_product_id(self):
        return PositiveInt(int(self.product_id))

    async def get_count(self):
        return PositiveInt(int(self.count))
