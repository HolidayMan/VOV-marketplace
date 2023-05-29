from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form
from pydantic import PositiveInt

from dependencies.auth import require_auth, require_role, get_user
from domain.user import UserRole, User
from services.customer_order_service import CustomerOrderService
from services.uow.cart.cart_unit_of_work import MySQLAsyncCartUnitOfWork
from services.uow.customer_order.customer_order_unit_of_work import MySQLAsyncCustomerOrderUnitOfWork

router = APIRouter()
service = CustomerOrderService(order_unit_of_work=MySQLAsyncCustomerOrderUnitOfWork(),
                               cart_unit_of_work=MySQLAsyncCartUnitOfWork())


@router.post("/makeOrder", name="makeOrder",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def make_order(request: Request, user: User = Depends(get_user)):
    pass


@router.get("/loadAllOrders", name="loadAllOrders",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_all_orders(request: Request, user: User = Depends(get_user)):
    pass


@router.get("/loadOrder", name="loadOrder",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_order(request: Request, user: User = Depends(get_user), orderId=Annotated[PositiveInt, Form()]):
    pass
