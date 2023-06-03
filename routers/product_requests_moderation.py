from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from starlette.responses import RedirectResponse

from dependencies.auth import require_auth, require_role
from domain.user import UserRole, User
from services.moderator_product_service import ModeratorProductService
from services.uow.moderator_product import MySQLAsyncModeratorProductUnitOfWork
from utils.templates import render

router = APIRouter(prefix='/moderator')
product_requests_service = ModeratorProductService(MySQLAsyncModeratorProductUnitOfWork())


@router.get('/product-requests-moderation', name='product-requests-moderation',
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.MODERATOR))])
async def product_requests_moderation(request: Request):
    requests = await product_requests_service.get_product_requests()
    return render(request, 'moderator/product_requests.html', {'requests': requests})


@router.get('/decline-product/{product_data_id}', name='decline-product',
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.MODERATOR))])
async def decline_product(request: Request, product_data_id: int):
    return render(request, 'moderator/decline_product_form.html', {'product_data_id': product_data_id})


@router.post('/decline-product/{product_data_id}', name='process-decline-product',
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.MODERATOR))])
async def process_decline_product(request: Request, product_data_id: int, refuse_reason: Annotated[str, Form()] = None,
                                  moderator: User = Depends(require_auth)):
    if not refuse_reason:
        return render(request, 'moderator/decline_product_form.html',
                      {'product_data_id': product_data_id, 'error': 'Refuse reason is required'})
    await product_requests_service.decline_product_request(product_data_id, refuse_reason, moderator)
    response = RedirectResponse(url=request.app.url_path_for('product-requests-moderation'), status_code=303)
    return response
