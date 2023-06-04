from typing import Annotated
from fastapi import APIRouter, Form, Depends, Request
from fastapi import status
from starlette.responses import RedirectResponse, HTMLResponse


from services.exceptions import DataAccessError, CannotCreateShopError
from services.seller_shop_service import SellerShopService
from services.uow.shop.shop_unit_of_work import MySQLAsyncShopUnitOfWork
from services.uow.shop_request.seller_shop_request_unit_of_work import MySQLAsyncSellerShopRequestUnitOfWork
from utils.templates import render
from dependencies.auth import get_user, require_auth, require_role
from domain.user import User, UserRole

router = APIRouter()
service = SellerShopService(MySQLAsyncShopUnitOfWork(), MySQLAsyncSellerShopRequestUnitOfWork())


@router.post("/createShop", name="createShop",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def create_shop(request: Request, name: Annotated[str, Form()],
                      description: Annotated[str, Form()], seller: User = Depends(get_user)):
    try:
        has_shop = await service.check_seller_has_shop(seller)
        if has_shop:
            return RedirectResponse(url=f"{router.url_path_for('seller_already_has_shop')}",
                                    status_code=status.HTTP_303_SEE_OTHER)
        has_request_in_process = await service.has_request_in_process(seller)
        if has_request_in_process:
            return render(request, "seller/load_shop.html", {"request_in_process": has_request_in_process})
        else:
            # Check if a record belongs to a user
            created_shop = await service.create_shop(name, description, seller)
            if created_shop.shop_data.id != seller.id:
                return HTMLResponse(content="Access denied", status_code=status.HTTP_403_FORBIDDEN)
            return RedirectResponse(url=f"{router.url_path_for('loadShop')}",
                                    status_code=status.HTTP_303_SEE_OTHER)
    except DataAccessError:
        return render(request, "data_access_error.html", {})
    except CannotCreateShopError:
        return RedirectResponse(url=f"{router.url_path_for('seller_already_has_shop')}",
                                    status_code=status.HTTP_303_SEE_OTHER)


# TODO check if seller has already created shop and his shop request in process.
#  If he does, redirect him to loadShop.html.

@router.get("/loadShopForm", name="loadShopForm",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def load_shop_form(request: Request):
    return render(request, "seller/create_shop.html", {})


# TODO check if seller has already created shop. If he does, redirect him to loadShop.html.


@router.get("/loadShop", name="loadShop",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def load_created_shop(request: Request, seller: User = Depends(get_user)):
    has_request_in_process = await service.has_request_in_process(seller)
    if has_request_in_process:
        return render(request, "seller/load_shop.html", {"request_in_process": has_request_in_process})
    shop = await service.get_shop_by_seller(seller)
    return render(request, "seller/load_shop.html", {"shop": shop})


# TODO you don`t have shop or all your shop request are declined
# if seller doesn`t have shop at all or he doesn`t have

@router.get("/seller_already_has_shop", name="seller_already_has_shop",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def load_shop(request: Request):
    return render(request, "seller/seller_already_has_shop.html", {})
