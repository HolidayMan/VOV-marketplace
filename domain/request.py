from pydantic import BaseModel
from pydantic.types import PositiveInt
from enum import Enum
from datetime import datetime
from domain.shop import ShopData
from domain.user import User


class RequestStatus(Enum):
    IN_PROCESS = "in_process"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class Request(BaseModel):
    id: PositiveInt
    seller_id: User
    moderator_id: User
    request_status: RequestStatus
    refuse_reason: str | None = None
    creation_date: datetime
    check_date: datetime | None = None


class ShopCreationRequest(Request):
    shop_data: ShopData
