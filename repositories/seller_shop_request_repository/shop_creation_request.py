from pydantic import PositiveInt

from domain.request import ShopCreationRequest


class ShopCreationRequestInDB(ShopCreationRequest):
    seller_id: PositiveInt
    moderator_id: PositiveInt | None

