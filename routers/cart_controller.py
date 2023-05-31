from typing import Annotated
from fastapi import APIRouter, Request, Depends, Form, status
from pydantic import PositiveInt
from starlette.responses import RedirectResponse
from app import app

from dependencies.auth import get_user, require_auth, require_role
from domain.user import User, UserRole
from forms.id_form import IdForm
from forms.product_count_form import ProductCountForm
from services.cart_service import CartService
from services.exceptions import DataAccessError
from services.uow.cart.cart_unit_of_work import MySQLAsyncCartUnitOfWork
from utils.templates import render

router = APIRouter()
service = CartService(MySQLAsyncCartUnitOfWork())


@router.get("/cart/", name="cart", dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def get_cart_items(request: Request, user: User = Depends(get_user)):
    try:
        items = await service.get_cart_items(user)
        return render(request, "customer/cart.html",
                      {"items_list": items})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.post("/addToCart", name="addToCart",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def add_product(request: Request,
                      user: User = Depends(get_user)):
    form = ProductCountForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            await service.add_product(user, await form.get_product_id(), await form.get_count())
            return RedirectResponse(url=f"{router.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
        except DataAccessError:
            return render(request, "data_access_error.html", {})
    return RedirectResponse(url=f"{app.url_path_for('catalog')}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/removeItemFromCart", name="removeItemFromCart",
             dependencies=[Depends(require_auth),
                           Depends(require_role(UserRole.CUSTOMER))])
async def remove_item(request: Request, user: User = Depends(get_user)):
    form = IdForm(request, "productId")
    await form.load_data()
    if await form.is_valid():
        try:
            await service.remove_item(user, await form.get_id())
            items = await service.get_cart_items(user)
            return render(request, "customer/cart.html",
                          {"items_list": items})
        except DataAccessError:
            return render(request, "data_access_error.html", {})
    else:
        return RedirectResponse(url=f"{router.url_path_for('cart')}", status_code=status.HTTP_303_SEE_OTHER)
