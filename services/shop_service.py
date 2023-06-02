from datetime import datetime

from pymysql import ProgrammingError, IntegrityError

from domain.request import RequestStatus
from domain.shop import Shop, ShopData
from domain.user import User
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB

from services.exceptions import DataAccessError, CannotCreateShopError
from services.uow.shop.shop_unit_of_work import AbstractShopUnitOfWork
from services.uow.shop_request.shop_request_unit_of_work import AbstractSellerShopRequestUnitOfWork


class ShopService:
    _shop_uow: AbstractShopUnitOfWork
    _shop_request_uow: AbstractSellerShopRequestUnitOfWork

    def __init__(self, unit_of_work: AbstractShopUnitOfWork, shop_request_uow: AbstractSellerShopRequestUnitOfWork):
        self._shop_uow = unit_of_work
        self._shop_request_uow = shop_request_uow

    async def create_shop(self, name: str, description: str, seller: User) -> Shop:
        try:
            can_create_shop = await self.check_seller_can_create_shop(seller)
            if not can_create_shop:
                raise CannotCreateShopError("Seller already has a shop")
            else:
                created_shop: Shop | None = None
                seller_has_shop = await self.check_seller_has_shop(seller)
                if seller_has_shop:
                    created_shop = await self.get_shop_by_seller(seller)
                async with self._shop_uow:
                    shop_data = await self._shop_uow.shop.create_shop_data(
                        shop_data=ShopData(name=name, description=description, approved=False))
                    if created_shop:
                        await self._shop_uow.shop.update_shop_date_id(created_shop.id, shop_data.id)
                    else:
                        created_shop = await self._shop_uow.shop.create_shop(Shop(id=seller.id, shop_data=shop_data))
                    async with self._shop_request_uow:
                        shop_request = ShopCreationRequestInDB(request_status=RequestStatus.IN_PROCESS,
                                                               creation_date=datetime.now(),
                                                               shop_data=created_shop.shop_data,
                                                               seller_id=seller.id)
                        await self._shop_request_uow.shop_request.create_shop_request(shop_request)
                        return created_shop
        except ProgrammingError:
            raise DataAccessError("Data access error")

    async def get_shop_by_seller(self, seller: User) -> Shop | None:
        try:
            async with self._shop_uow:
                shop = await self._shop_uow.shop.get_shop_by_seller(seller)
                return shop
        except ProgrammingError:
            raise DataAccessError("Data access error")

    async def check_seller_has_shop(self, seller: User) -> bool:
        try:
            async with self._shop_uow:
                existing_shop = await self._shop_uow.shop.get_shop_by_seller(seller)
                return existing_shop is not None
        except ProgrammingError:
            raise DataAccessError("Data access error")

    async def check_seller_can_create_shop(self, seller: User) -> bool:
        async with self._shop_request_uow:
            async with self._shop_uow:
                shop = await self._shop_uow.shop.get_shop_by_seller(seller)
                if shop is None:
                    return True
                shop_requests = await self._shop_request_uow.shop_request.get_all_shop_requests(seller)
                for request in shop_requests:
                    if request.request_status is not RequestStatus.DECLINED:
                        return False

    async def create_shop_request(self, shop_data: ShopData):
        pass
