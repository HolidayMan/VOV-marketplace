from money import Money
from pydantic import PositiveInt
from aiomysql.cursors import DictCursor

from domain.order import OrderItemStatus
from domain.product import ProductData, Product
from domain.user import User
from repositories.exceptions import DoesNotExistError
from repositories.order.exceptions import OrderItemDoesNotExistError
from repositories.order.order import OrderItemWithOrderIdAndCreationDate
from repositories.order.seller_order.seller_order_repository import AsyncSellerOrderRepository
from repositories.order.seller_order.sql import GET_ORDER_ITEMS_BY_SELLER_ID, \
    GET_ORDER_ITEM_BY_ORDER_AND_PRODUCT_IDS, \
    UPDATE_ORDER_ITEM_BY_ORDER_AND_PRODUCT_IDS, GET_SELLER_ID_BY_PRODUCT_ID, GET_NOT_PROCESSED_ORDER_ITEMS_BY_SELLER_ID


def map_row_to_order_item(row):
    return OrderItemWithOrderIdAndCreationDate(
        refuse_reason=row['refuse_reason'],
        product=Product(
            id=PositiveInt(row['product_id']),
            price=Money(row['product_price'], 'UAH'),
            product_data=ProductData(
                id=PositiveInt(row['product_data_id']),
                name=row['product_name'],
                description=row['description'],
                image_file_path=row['image_file_path'],
                approved=row['approved']
            )
        ),
        price=Money(row['item_price'], 'UAH'),
        check_date=row['check_date'],
        status=OrderItemStatus(row['status_name']),
        count=PositiveInt(row['count']),
        order_id=PositiveInt(row['order_id']),
        creation_date=row['creation_date']
    )


def map_rows_to_order_items_list(item_rows) -> list[OrderItemWithOrderIdAndCreationDate]:
    items_list = []
    for row in item_rows:
        item = map_row_to_order_item(row)
        items_list.append(item)
    return items_list


class MySQLAsyncSellerOrderRepository(AsyncSellerOrderRepository):

    def __init__(self, cursor: DictCursor):
        self.cursor = cursor

    async def get_not_processed_ordered_items(self, seller: User) -> list[OrderItemWithOrderIdAndCreationDate]:
        await self.cursor.execute(
            GET_NOT_PROCESSED_ORDER_ITEMS_BY_SELLER_ID,
            (seller.id,)
        )
        if order_items_rows := await self.cursor.fetchall():
            items_list = map_rows_to_order_items_list(order_items_rows)
            return items_list
        return []

    async def get_ordered_items_list(self, seller: User) -> list[OrderItemWithOrderIdAndCreationDate]:
        await self.cursor.execute(
            GET_ORDER_ITEMS_BY_SELLER_ID,
            (seller.id,)
        )
        if order_items_rows := await self.cursor.fetchall():
            items_list = map_rows_to_order_items_list(order_items_rows)
            return items_list
        return []

    async def get_ordered_item(self, order_id: PositiveInt,
                               product_id: PositiveInt) -> OrderItemWithOrderIdAndCreationDate:
        await self.cursor.execute(
            GET_ORDER_ITEM_BY_ORDER_AND_PRODUCT_IDS,
            (order_id, product_id)
        )
        if order_item_row := await self.cursor.fetchone():
            item = map_row_to_order_item(order_item_row)
            return item
        raise OrderItemDoesNotExistError("Order item does not exist")

    async def update_order_item(self,
                                order_item: OrderItemWithOrderIdAndCreationDate) -> OrderItemWithOrderIdAndCreationDate:
        await self.cursor.execute(
            UPDATE_ORDER_ITEM_BY_ORDER_AND_PRODUCT_IDS,
            (order_item.status.name, order_item.check_date, order_item.refuse_reason,
             order_item.order_id, order_item.product.id)
        )
        return await self.get_ordered_item(order_item.order_id, order_item.product.id)

    async def get_seller_id_for_product(self, product_id) -> PositiveInt:
        await self.cursor.execute(
            GET_SELLER_ID_BY_PRODUCT_ID,
            (product_id,)
        )
        if id_row := await self.cursor.fetchone():
            seller_id = PositiveInt(id_row['seller_id'])
            return seller_id
        raise DoesNotExistError("No product with such id")
