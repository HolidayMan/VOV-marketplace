from pydantic import PositiveInt

from domain.request import ShopCreationRequest, RequestStatus


class ShopCreationRequestInDB(ShopCreationRequest):
    seller_id: PositiveInt
    moderator_id: PositiveInt | None

    def request_in_process(self) -> bool:
        return self.request_status == RequestStatus.IN_PROCESS

