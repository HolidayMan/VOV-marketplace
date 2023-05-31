from fastapi import APIRouter, Depends, Request
from pydantic import PositiveInt
from starlette import status
from starlette.responses import RedirectResponse

from app import app
from dependencies.auth import require_auth, require_role, get_user
from domain.user import UserRole, User

router = APIRouter()


class InvalidOrderItemIdException(Exception):
    pass


async def validate_order_item_id(itemId: str) -> PositiveInt:
    if not str.isnumeric(itemId) or not (int(itemId) > 1):
        raise InvalidOrderItemIdException
    return PositiveInt(itemId)


@app.exception_handler(InvalidOrderItemIdException)
async def invalid_id_exception_handler(request: Request, exc: InvalidOrderItemIdException):
    return RedirectResponse(url=f"{router.url_path_for('loadOrderedItems')}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/seller/loadOrderedItems", name="loadOrderedItems",
            dependencies=[Depends(require_auth),
                          Depends(require_role(UserRole.SELLER))])
async def load_ordered_items(seller: User = Depends(get_user)):
    pass


@router.get("/seller/getOrderedItem", name="getOrderedItem",
            dependencies=[Depends(require_auth),
                          Depends(require_role(UserRole.SELLER))])
async def get_ordered_item(seller: User = Depends(get_user), itemId: PositiveInt = Depends(validate_order_item_id)):
    pass


@router.post("/seller/acceptOrder", name="acceptOrder",
             dependencies=[Depends(require_auth),
                           Depends(require_role(UserRole.SELLER))])
async def accept_order(seller: User = Depends(get_user), itemId: PositiveInt = Depends(validate_order_item_id)):
    pass


@router.post("/seller/declineOrder", name="declineOrder",
             dependencies=[Depends(require_auth),
                           Depends(require_role(UserRole.SELLER))])
async def decline_order(refuse_reason: str, seller: User = Depends(get_user),
                        itemId: PositiveInt = Depends(validate_order_item_id)):
    pass
