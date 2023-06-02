from datetime import datetime

from pydantic import PositiveInt
from pymysql import DatabaseError

from domain.order import OrderItemStatus
from domain.user import User
from repositories.exceptions import DoesNotExistError
from repositories.order.exceptions import CannotProcessOrderItemError
from repositories.order.order import OrderItemWithOrderIdAndCreationDate
from services.exceptions import DataAccessError, InvalidUserError
from services.uow.seller_order.seller_order_unit_of_work import AbstractSellerOrderUnitOfWork


class SellerOrderService:
    _uow: AbstractSellerOrderUnitOfWork

    def __init__(self, unit_of_work: AbstractSellerOrderUnitOfWork):
        self._uow = unit_of_work

    async def get_ordered_items(self, seller: User) -> list[OrderItemWithOrderIdAndCreationDate]:
        try:
            async with self._uow:
                items = await self._uow.orders.get_ordered_items_list(seller)
                return items
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def get_not_processed_ordered_items(self, seller: User) -> list[OrderItemWithOrderIdAndCreationDate]:
        try:
            async with self._uow:
                items = await self._uow.orders.get_not_processed_ordered_items(seller)
                return items
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def get_ordered_item(self, product_id: PositiveInt,
                               order_id: PositiveInt, seller: User) -> OrderItemWithOrderIdAndCreationDate:
        if not await self.product_belongs_to_seller(product_id, seller.id):
            raise InvalidUserError("Invalid seller id")
        try:
            async with self._uow:
                item = await self._uow.orders.get_ordered_item(order_id, product_id)
                return item
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def accept_order(self, product_id: PositiveInt,
                           order_id: PositiveInt, seller: User) -> OrderItemWithOrderIdAndCreationDate:
        try:
            if await self.can_process_order(product_id, order_id):
                order_item = await self.get_ordered_item(product_id, order_id, seller)
                async with self._uow:
                    order_item.status = OrderItemStatus.ACCEPTED
                    order_item.check_date = datetime.now()
                    await self._uow.orders.update_order_item(order_item)
                    await self._uow.commit()
                    return order_item
            raise CannotProcessOrderItemError("Cannot accept order item as its status is not IN_PROCESS")
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def decline_order(self, product_id: PositiveInt,
                            order_id: PositiveInt,
                            refuse_reason: str, seller: User) -> OrderItemWithOrderIdAndCreationDate:
        try:
            if await self.can_process_order(product_id, order_id):
                order_item = await self.get_ordered_item(product_id, order_id, seller)
                async with self._uow:
                    order_item.status = OrderItemStatus.DECLINED
                    order_item.check_date = datetime.now()
                    order_item.refuse_reason = refuse_reason
                    await self._uow.orders.update_order_item(order_item)
                    await self._uow.commit()
                    return order_item
            raise CannotProcessOrderItemError("Cannot decline order item as its status is not IN_PROCESS")
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def can_process_order(self, product_id: PositiveInt, order_id: PositiveInt) -> bool:
        try:
            async with self._uow:
                item = await self._uow.orders.get_ordered_item(order_id, product_id)
                return item.can_be_processed()
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def product_belongs_to_seller(self, product_id: PositiveInt, seller_id: PositiveInt) -> bool:
        try:
            async with self._uow:
                seller_id_in_db = await self._uow.orders.get_seller_id_for_product(product_id)
                return seller_id == seller_id_in_db
        except DatabaseError:
            raise DataAccessError("Data access error")
        except DoesNotExistError:
            return False
