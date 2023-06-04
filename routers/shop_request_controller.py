from typing import Annotated

from fastapi import APIRouter, Form, Depends, Request, HTTPException
from pydantic import PositiveInt
from starlette import status
from starlette.responses import RedirectResponse

from dependencies.auth import require_auth, require_role, get_user
from domain.user import UserRole, User
from services.exceptions import DataAccessError
from services.moderator_shop_service import ModeratorShopService
from services.uow.shop.shop_unit_of_work import MySQLAsyncShopUnitOfWork
from services.uow.shop_request.moderator_shop_request_unit_of_work import MySQLAsyncModeratorShopRequestUnitOfWork
from utils.templates import render

router = APIRouter()
service = ModeratorShopService(MySQLAsyncShopUnitOfWork(), MySQLAsyncModeratorShopRequestUnitOfWork())


@router.get("/moderator/viewShopRequests", name="viewShopRequests",
            dependencies=[Depends(require_auth),
                          Depends(require_role(UserRole.MODERATOR))])
async def load_all_shop_requests(request: Request):
    try:
        all_shop_requests = await service.get_all_shop_requests()
        return render(request, "moderator/shop_requests_list.html", {"shop_requests_list": all_shop_requests})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.get("/moderator/viewShopRequest", name="viewShopRequest",
            dependencies=[Depends(require_auth),
                          Depends(require_role(UserRole.MODERATOR))])
async def load_shop_request(request: Request, shop_data_id: PositiveInt):
    shop_request = await service.get_shop_request(shop_data_id)
    return render(request, "moderator/view_shop_request.html", {"shop_request": shop_request})


@router.post("/moderator/approveShopRequest/{shop_data_id}", name="approveShopRequest",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.MODERATOR))])
async def approve_shop_request(request: Request, shop_data_id: PositiveInt, moderator: User = Depends(get_user)):
    try:
        await service.approve_shop_request(shop_data_id, moderator)
        response = RedirectResponse(url=request.app.url_path_for('viewShopRequests'), status_code=303)
        return response
    except DataAccessError:
        return render(request, "data_access_error.html", {})


@router.post("/moderator/declineShopRequest{shop_data_id}", name="declineShopRequest",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.MODERATOR))])
async def decline_shop_request(request: Request, shop_data_id: PositiveInt, refuse_reason: Annotated[str, Form()],
                               moderator: User = Depends(get_user)):
    if not refuse_reason:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refuse reason is required")
    await service.decline_shop_request(shop_data_id, refuse_reason, moderator)
    response = RedirectResponse(url=request.app.url_path_for('viewShopRequests'), status_code=303)
    return response
