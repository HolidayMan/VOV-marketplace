from fastapi import APIRouter, Depends, Request, status
from pydantic import PositiveInt
from starlette.responses import RedirectResponse

from app import app
from dependencies.auth import require_auth, require_role, get_user
from domain.user import UserRole, User
from repositories.order.exceptions import OrderDoesNotExist
from services.customer_order_service import CustomerOrderService
from services.exceptions import DataAccessError
from services.uow.cart.cart_unit_of_work import MySQLAsyncCartUnitOfWork
from services.uow.customer_order.customer_order_unit_of_work import MySQLAsyncCustomerOrderUnitOfWork
from utils.templates import render

router = APIRouter()
service = CustomerOrderService(order_unit_of_work=MySQLAsyncCustomerOrderUnitOfWork(),
                               cart_unit_of_work=MySQLAsyncCartUnitOfWork())


class InvalidCustomerOrderIdException(Exception):
    pass


async def validate_order_id(orderId: str) -> PositiveInt:
    if not str.isnumeric(orderId) or not (int(orderId) > 1):
        raise InvalidCustomerOrderIdException
    return PositiveInt(orderId)


@app.exception_handler(InvalidCustomerOrderIdException)
async def invalid_id_exception_handler(request: Request, exc: InvalidCustomerOrderIdException):
    return RedirectResponse(url=f"{router.url_path_for('loadAllOrders')}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/customer/makeOrder", name="makeOrder",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def make_order(request: Request, user: User = Depends(get_user)):
    try:
        if not service.can_make_order(user):
            return RedirectResponse(url=f"{app.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
        created_order = await service.make_order(user)
        return render(request, "customer/view_order.html", {"order": created_order})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.get("/customer/previewOrder", name="previewOrder",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def preview_order(request: Request, user: User = Depends(get_user)):
    try:
        if not service.can_make_order(user):
            return RedirectResponse(url=f"{app.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
        order_preview = await service.get_order_preview(user)
        return render(request, "customer/order_preview.html", {"order": order_preview})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.get("/customer/loadAllOrders", name="loadAllOrders",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_all_orders(request: Request, user: User = Depends(get_user)):
    try:
        orders = await service.get_all_orders(user)
        return render(request, "customer/customer_orders.html", {"orders_list": orders})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.get("/customer/loadOrder/", name="loadOrder",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_order(request: Request, orderId: PositiveInt = Depends(validate_order_id), user: User = Depends(get_user)):
    try:
        order = await service.get_order(orderId)
        return render(request, "customer/view_order.html", {"order": order})
    except DataAccessError:
        return render(request, "data_access_error.html", {})
    except OrderDoesNotExist:
        return RedirectResponse(url=f"{router.url_path_for('loadAllOrders')}", status_code=status.HTTP_303_SEE_OTHER)
