from fastapi import APIRouter, Depends, Request, status
from pydantic import PositiveInt
from starlette.responses import RedirectResponse

from app import app
from dependencies.auth import require_auth, require_role, get_user
from domain.user import UserRole, User
from forms.id_form import IdForm
from repositories.order.exceptions import OrderDoesNotExistError
from services.customer_order_service import CustomerOrderService
from services.exceptions import DataAccessError, InvalidUserError, CannotCancelOrderError
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
    return redirect_to_orders_list()


@app.exception_handler(OrderDoesNotExistError)
async def invalid_id_exception_handler(request: Request, exc: OrderDoesNotExistError):
    return redirect_to_orders_list()


def redirect_to_orders_list():
    return RedirectResponse(url=f"{router.url_path_for('loadAllOrders')}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/customer/makeOrder", name="makeOrder",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def make_order(request: Request, user: User = Depends(get_user)):
    if not service.can_make_order(user):
        return RedirectResponse(url=f"{app.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
    created_order = await service.make_order(user)
    return render(request, "customer/view_order.html", {"order": created_order})


@router.get("/customer/previewOrder", name="previewOrder",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def preview_order(request: Request, user: User = Depends(get_user)):
    if not service.can_make_order(user):
        return RedirectResponse(url=f"{app.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
    order_preview = await service.get_order_preview(user)
    return render(request, "customer/order_preview.html", {"order": order_preview})


@router.get("/customer/loadAllOrders", name="loadAllOrders",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_all_orders(request: Request, user: User = Depends(get_user)):
    orders = await service.get_all_orders(user)
    return render(request, "customer/customer_orders.html", {"orders_list": orders})


@router.get("/customer/loadOrder/", name="loadOrder",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def load_order(request: Request, orderId: PositiveInt = Depends(validate_order_id), user: User = Depends(get_user)):
    try:
        order = await service.get_order(orderId, user)
        return render(request, "customer/view_order.html", {"order": order})
    except InvalidUserError:
        return redirect_to_orders_list()


@router.post("/customer/cancelOrder/", name="cancelOrder",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def cancel_order(request: Request, user: User = Depends(get_user)):
    try:
        form = IdForm(request, "orderId")
        await form.load_data()
        if form.is_valid():
            canceled_order = await service.cancel_order(form.get_id(), user)
            return render(request, "customer/view_order.html", {"order": canceled_order})
    except InvalidUserError:
        return redirect_to_orders_list()
    except CannotCancelOrderError:
        return redirect_to_orders_list()


