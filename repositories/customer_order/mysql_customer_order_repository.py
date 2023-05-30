from datetime import datetime

from money import Money
from pydantic import PositiveInt

from db import AsyncSession
from domain.order import Order, OrderStatus, OrderItem, OrderItemStatus
from domain.product import Product, ProductData
from domain.user import User
from repositories.customer_order.customer_order_repository import AsyncCustomerOrderRepository
from repositories.customer_order.exceptions import OrderDoesNotExist
from repositories.customer_order.sql import CREATE_ORDER, CREATE_ORDER_ITEM, GET_ORDER_BY_ID, \
    GET_ORDER_ITEMS_BY_ORDER_ID, GET_ORDER_IDS_FOR_USER

DATE_TIME_FORMAT_STR = '%Y-%m-%d %H:%M:%S'


def map_row_to_order(row) -> Order:
    return Order(
        user_id=PositiveInt(row['customer_id']),
        id=PositiveInt(row['id']),
        order_items=[],
        status=OrderStatus[row['status_name']],
        creation_date=datetime.strptime(row['creation_date'], DATE_TIME_FORMAT_STR)
    )


def map_rows_to_order_items_list(item_rows) -> list[OrderItem]:
    items_list = []
    for row in item_rows:
        item = OrderItem(
            refuse_reason=row['refuse_reason'],
            product=Product(
                id=PositiveInt(row['product_id']),
                price=Money(row['product.price'], 'UAH'),
                shop_id=PositiveInt(row['seller_id']),
                product_data=ProductData(
                    id=PositiveInt(row['product_data_id']),
                    name=row['product_data.name'],
                    description=row['description'],
                    image_file_path=row['image_file_path'],
                    approved=row['approved']
                )
            ),
            price=Money(row['order_item.price'], 'UAH'),
            check_date=datetime.strptime(row['check_date'], DATE_TIME_FORMAT_STR),
            status=OrderItemStatus(row['order_item_status.name']),
            count=PositiveInt(row['count'])
        )
        items_list.append(item)
    return items_list


def map_ids_rows_to_ids_list(ids_rows) -> list[PositiveInt]:
    ids = []
    for id_row in ids_rows:
        id_item = PositiveInt(id_row['id'])
        ids.append(id_item)
    return ids


class MySQLAsyncCustomerOrderRepository(AsyncCustomerOrderRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_orders(self, user: User) -> list[Order]:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                GET_ORDER_IDS_FOR_USER,
                (user.id,)
            )
            orders_list = []
            if ids_rows := cursor.fetchall():
                ids = map_ids_rows_to_ids_list(ids_rows)
                for order_id in ids:
                    orders_list.append(await self.get_order(order_id))
            return orders_list

    async def get_order(self, orderId: PositiveInt) -> Order:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                GET_ORDER_BY_ID,
                (orderId,)
            )
            if order_row := await cursor.fetchall():
                order = map_row_to_order(order_row)
                await cursor.execute(
                    GET_ORDER_ITEMS_BY_ORDER_ID,
                    (orderId,)
                )
                if order_items_rows := await cursor.fetchall():
                    order_items_list = map_rows_to_order_items_list(order_items_rows)
                    order.order_items = order_items_list
                return order
            raise OrderDoesNotExist("There is no order with this id")

    async def add_order(self, order: Order) -> Order:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                CREATE_ORDER,
                (order.status.name, order.user_id, order.creation_date)
            )
            order.id = PositiveInt(cursor.lastrowid)
            for order_item in order.order_items:
                await cursor.execute(
                    CREATE_ORDER_ITEM,
                    (order.id, order_item.count, order_item.price.amount, order_item.product.id, order_item.status.name)
                )
            await self.session.commit()
            return order
