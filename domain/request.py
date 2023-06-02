from pydantic import BaseModel, PositiveInt
from enum import Enum
from datetime import datetime

from domain.product import ProductData
from .shop import ShopData
from domain.user import User


class RequestStatus(Enum):
    IN_PROCESS = "in_process"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class Request(BaseModel):
    seller_id: User
    moderator_id: User | None
    request_status: RequestStatus
    refuse_reason: str | None = None
    creation_date: datetime
    check_date: datetime | None = None


class ShopCreationRequest(BaseModel):
    request_status: RequestStatus
    refuse_reason: str | None = None
    creation_date: datetime
    check_date: datetime | None = None
    shop_data: ShopData


class ProductCreationRequest(Request):
    product_data: ProductData

    # delete in request id and create ShopCreationRequest in db
    #TODO create normal base class!