from money import Money
from pydantic import PositiveInt

from db import AsyncSession
from domain.order import Order, OrderStatus, OrderItem, OrderItemStatus
from domain.product import Product, ProductData
from domain.user import User
from repositories.order.customer_order.customer_order_repository import AsyncCustomerOrderRepository
from repositories.order.exceptions import OrderDoesNotExistError
from repositories.order.customer_order.sql import CREATE_ORDER, CREATE_ORDER_ITEM, GET_ORDER_BY_ID, \
    GET_ORDER_ITEMS_BY_ORDER_ID, GET_ORDER_IDS_FOR_USER, UPDATE_ORDER_STATUS
from repositories.order.order import OrderWithUserId

DATE_TIME_FORMAT_STR = '%Y-%m-%d %H:%M:%S'


def map_row_to_order(row) -> OrderWithUserId:
    return OrderWithUserId(
        id=PositiveInt(row['id']),
        order_items=[],
        status=OrderStatus(row['status_name']),
        creation_date=row['creation_date'],
        user_id=row['customer_id']
    )


def map_rows_to_order_items_list(item_rows) -> list[OrderItem]:
    items_list = []
    for row in item_rows:
        item = OrderItem(
            refuse_reason=row['refuse_reason'],
            product=Product(
                id=PositiveInt(row['product_id']),
                price=Money(row['product_price'], 'UAH'),
                product_data=ProductData(
                    id=PositiveInt(row['product_data_id']),
                    name=row['name'],
                    description=row['description'],
                    image_file_path=row['image_file_path'],
                    approved=row['approved']
                )
            ),
            price=Money(row['item_price'], 'UAH'),
            check_date=row['check_date'],
            status=OrderItemStatus(row['status_name']),
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

    async def get_all_orders(self, user: User) -> list[OrderWithUserId]:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                GET_ORDER_IDS_FOR_USER,
                (user.id,)
            )
            orders_list = []
            if ids_rows := await cursor.fetchall():
                ids = map_ids_rows_to_ids_list(ids_rows)
                for order_id in ids:
                    orders_list.append(await self.get_order(order_id))
            return orders_list

    async def get_order(self, orderId: PositiveInt) -> OrderWithUserId:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                GET_ORDER_BY_ID,
                (orderId,)
            )
            if order_row := await cursor.fetchone():
                order = map_row_to_order(order_row)
                await cursor.execute(
                    GET_ORDER_ITEMS_BY_ORDER_ID,
                    (orderId,)
                )
                if order_items_rows := await cursor.fetchall():
                    order_items_list = map_rows_to_order_items_list(order_items_rows)
                    order.order_items = order_items_list
                return order
            raise OrderDoesNotExistError("There is no order with this id")

    async def add_order(self, order: Order, user: User) -> OrderWithUserId:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                CREATE_ORDER,
                (order.status.name, user.id, order.creation_date)
            )
            order.id = PositiveInt(cursor.lastrowid)
            for order_item in order.order_items:
                await cursor.execute(
                    CREATE_ORDER_ITEM,
                    (order.id, order_item.count, order_item.price.amount, order_item.product.id, order_item.status.name)
                )
            await self.session.commit()
            return OrderWithUserId(
                id=order.id,
                order_items=order.order_items,
                status=order.status,
                creation_date=order.creation_date,
                user_id=user.id
            )

    async def cancel_order(self, orderId: PositiveInt) -> OrderWithUserId:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                UPDATE_ORDER_STATUS,
                (OrderStatus.CANCELED.name, orderId)
            )
            await self.session.commit()
            return await self.get_order(orderId)
