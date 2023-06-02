from fastapi import APIRouter, Depends, Request
from pydantic import PositiveInt
from starlette import status
from starlette.responses import RedirectResponse

from app import app
from dependencies.auth import require_auth, require_role, get_user
from domain.user import UserRole, User
from forms.order_item_form import OrderItemForm, DeclineOrderItemForm
from repositories.order.exceptions import OrderItemDoesNotExistError, CannotProcessOrderItemError
from services.exceptions import DataAccessError, InvalidUserError
from services.seller_order_service import SellerOrderService
from services.uow.seller_order.seller_order_unit_of_work import MySQLAsyncSellerOrderUnitOfWork
from utils.templates import render

router = APIRouter()
service = SellerOrderService(MySQLAsyncSellerOrderUnitOfWork())


class InvalidOrderItemIdException(Exception):
    pass


def validate_id_str(id_str: str) -> PositiveInt:
    if not str.isnumeric(id_str) or not (int(id_str) >= 1):
        raise InvalidOrderItemIdException
    return PositiveInt(id_str)


def validate_product_id(product_id: str) -> PositiveInt:
    return validate_id_str(product_id)


def validate_order_id(order_id: str) -> PositiveInt:
    return validate_id_str(order_id)


@app.exception_handler(InvalidOrderItemIdException)
async def invalid_id_exception_handler(request: Request, exc: InvalidOrderItemIdException):
    return redirect_to_items_list()


@app.exception_handler(OrderItemDoesNotExistError)
async def order_item_does_not_exist_exception_handler(request: Request, exc: OrderItemDoesNotExistError):
    return redirect_to_items_list()


def redirect_to_items_list():
    return RedirectResponse(url=f"{router.url_path_for('loadOrderedItems')}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/seller/loadOrderedItems", name="loadOrderedItems",
            dependencies=[Depends(require_auth),
                          Depends(require_role(UserRole.SELLER))])
async def load_ordered_items(request: Request, seller: User = Depends(get_user)):
    items = await service.get_ordered_items(seller)
    return render(request, "/seller/ordered_items_list.html", {"order_items_list": items})


@router.get("/seller/getOrderedItem", name="getOrderedItem",
            dependencies=[Depends(require_auth),
                          Depends(require_role(UserRole.SELLER))])
async def get_ordered_item(request: Request,
                           order_id: PositiveInt = Depends(validate_order_id),
                           product_id: PositiveInt = Depends(validate_product_id),
                           seller: User = Depends(get_user)):
    try:
        item = await service.get_ordered_item(product_id, order_id, seller)
        return render(request, "/seller/view_order_item.html", {"order_item": item})
    except InvalidUserError:
        return redirect_to_items_list()


@router.post("/seller/acceptOrder", name="acceptOrder",
             dependencies=[Depends(require_auth),
                           Depends(require_role(UserRole.SELLER))])
async def accept_order(request: Request, seller: User = Depends(get_user)):
    form = OrderItemForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            order_item = await service.accept_order(order_id=form.get_order_id(),
                                                    product_id=form.get_product_id(), seller=seller)
            return render(request, "/seller/view_order_item.html", {"order_item": order_item})
        except CannotProcessOrderItemError:
            return redirect_to_items_list()
        except InvalidUserError:
            return redirect_to_items_list()
    return redirect_to_items_list()


@router.post("/seller/declineOrder", name="declineOrder",
             dependencies=[Depends(require_auth),
                           Depends(require_role(UserRole.SELLER))])
async def decline_order(request: Request, seller: User = Depends(get_user)):
    form = DeclineOrderItemForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            order_item = await service.decline_order(order_id=form.get_order_id(),
                                                     product_id=form.get_product_id(),
                                                     refuse_reason=form.get_refuse_reason(),
                                                     seller=seller)
            return render(request, "/seller/view_order_item.html", {"order_item": order_item})
        except CannotProcessOrderItemError:
            return redirect_to_items_list()
        except InvalidUserError:
            return redirect_to_items_list()
    elif form.errors.get('product_id') or form.errors.get('order_id'):
        return redirect_to_items_list()
    else:
        order_item = await service.get_ordered_item(order_id=form.get_order_id(),
                                                    product_id=form.get_product_id(),
                                                    seller=seller)
        return render(request, "/seller/view_order_item.html", {"order_item": order_item, "form": form})
