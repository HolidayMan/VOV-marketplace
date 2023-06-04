from datetime import datetime

from pydantic import PositiveInt
from pymysql import DatabaseError

from domain.user import User
from repositories.exceptions import CannotProcessShopRequestError
from repositories.order.exceptions import CannotProcessOrderItemError
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB
from services.exceptions import DataAccessError
from services.uow.shop.shop_unit_of_work import AbstractShopUnitOfWork
from services.uow.shop_request.moderator_shop_request_unit_of_work import AbstractModeratorShopRequestUnitOfWork


class ModeratorShopService:
    _shop_uow: AbstractShopUnitOfWork
    _moderator_shop_request_uow: AbstractModeratorShopRequestUnitOfWork

    def __init__(self, unit_of_work: AbstractShopUnitOfWork,
                 _moderator_shop_request_uow: AbstractModeratorShopRequestUnitOfWork):
        self._shop_uow = unit_of_work
        self._moderator_shop_request_uow = _moderator_shop_request_uow

    async def get_all_shop_requests(self) -> list[ShopCreationRequestInDB]:
        try:
            async with self._moderator_shop_request_uow:
                shop_requests = await self._moderator_shop_request_uow.shop_request.get_shop_requests_list()
                return shop_requests
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def get_shop_request(self, shop_data_id: PositiveInt) -> ShopCreationRequestInDB:
        try:
            async with self._moderator_shop_request_uow:
                request = await self._moderator_shop_request_uow.shop_request.get_shop_request(shop_data_id)
                return request
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def approve_shop_request(self, shop_data_id: PositiveInt, moderator: User) -> None:
        try:
            if not await self.shop_request_in_process(shop_data_id):
                raise CannotProcessOrderItemError("Cannot approve order item as its status is not IN_PROCESS")
            async with self._moderator_shop_request_uow:
                check_date = datetime.now()
                await self._moderator_shop_request_uow.shop_request.approve_shop_request(
                    shop_data_id, moderator, check_date)
                await self._moderator_shop_request_uow.commit()
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def decline_shop_request(self,
                                   shop_data_id: PositiveInt, refuse_reason: str, moderator: User) \
            -> None:
        try:
            async with self._moderator_shop_request_uow:
                check_date = datetime.now()
                await self._moderator_shop_request_uow.shop_request.decline_shop_request(
                    shop_data_id, refuse_reason, moderator, check_date)
                await self._moderator_shop_request_uow.commit()
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def shop_request_in_process(self, shop_data_id: PositiveInt) -> bool:
        try:
            async with self._moderator_shop_request_uow:
                shop_request = await self._moderator_shop_request_uow.shop_request.get_shop_request(shop_data_id)
                return shop_request.request_in_process()
        except DatabaseError:
            raise DataAccessError("Data access error")
