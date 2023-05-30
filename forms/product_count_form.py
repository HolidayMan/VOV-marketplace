from typing import List, Optional

from fastapi import Request


class ProductCountForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.count: Optional[int] = None
        self.product_id: Optional[int] = None

    async def load_data(self):
        form = await self.request.form()
        self.count = int(form.get("count"))
        self.product_id = int(form.get("product_id"))

    async def is_valid(self):
        if not self.count or not (self.count >= 1):
            self.errors.append("Count must be more than 1")
        if not self.product_id or not (self.product_id >= 1):
            self.errors.append("Invalid product id")
        if not self.errors:
            return True
        return False
