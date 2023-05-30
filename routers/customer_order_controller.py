from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form, status
from pydantic import PositiveInt
from starlette.responses import RedirectResponse

from app import app
from dependencies.auth import require_auth, require_role, get_user
from domain.user import UserRole, User
from services.customer_order_service import CustomerOrderService
from services.exceptions import DataAccessError
from services.uow.cart.cart_unit_of_work import MySQLAsyncCartUnitOfWork
from services.uow.customer_order.customer_order_unit_of_work import MySQLAsyncCustomerOrderUnitOfWork
from utils.templates import render

router = APIRouter()
service = CustomerOrderService(order_unit_of_work=MySQLAsyncCustomerOrderUnitOfWork(),
                               cart_unit_of_work=MySQLAsyncCartUnitOfWork())


@router.post("/makeOrder", name="makeOrder",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def make_order(request: Request, user: User = Depends(get_user)):
    try:
        if not service.can_make_order(user):
            return RedirectResponse(url=f"{app.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
        created_order = await service.make_order(user)
        return render(request, "customer/view_order.html", {"order": created_order})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.get("/previewOrder", name="previewOrder",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def preview_order(request: Request, user: User = Depends(get_user)):
    try:
        if not service.can_make_order(user):
            return RedirectResponse(url=f"{app.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
        order_preview = await service.get_order_preview(user)
        return render(request, "customer/order_preview.html", {"order": order_preview})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.get("/loadAllOrders", name="loadAllOrders",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_all_orders(request: Request, user: User = Depends(get_user)):
    pass


@router.get("/loadOrder", name="loadOrder",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_order(request: Request, user: User = Depends(get_user), orderId=Annotated[PositiveInt, Form()]):
    pass
