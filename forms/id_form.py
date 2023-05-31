from typing import List, Optional

from fastapi import Request
from pydantic import PositiveInt


class IdForm:
    def __init__(self, request: Request, id_name: str):
        self.request: Request = request
        self.errors: List = []
        self.id: Optional[str] = None
        self.id_name = id_name

    async def load_data(self):
        form = await self.request.form()
        self.id = form.get(self.id_name)

    async def is_valid(self):
        if not self.id or not str.isnumeric(self.id) or not (int(self.id) >= 1):
            self.errors.append("Id must number be bigger than 1")
        if not self.errors:
            return True
        return False

    async def get_id(self):
        return PositiveInt(self.id)
