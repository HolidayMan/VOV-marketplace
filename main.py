from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from fastapi import Request
from auth.middleware import process_unauthorized_error, process_forbidden_error
from routers import catalog_controller, cart_controller, shop_controller, \
    customer_order_controller, product_management_controller, seller_order_controller, shop_request_controller, \
    product_requests_moderation
from auth.router import router as auth_router
from services.exceptions import DataAccessError
from settings import STATIC_ROOT, STATIC_URL, MEDIA_ROOT, MEDIA_URL
from app import app
from utils.templates import render

app.include_router(shop_request_controller.router)
app.include_router(seller_order_controller.router)
app.include_router(catalog_controller.router)
app.include_router(cart_controller.router)
app.include_router(shop_controller.router)
app.include_router(product_management_controller.router)
app.include_router(customer_order_controller.router)
app.include_router(product_requests_moderation.router)
app.include_router(auth_router)
app.mount(STATIC_URL, StaticFiles(directory=STATIC_ROOT), name="static")
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name="media")


@app.get("/")
async def root():
    return RedirectResponse(url=app.url_path_for("catalog"), status_code=302)


@app.exception_handler(DataAccessError)
async def data_access_error_exception_handler(request: Request, exc: DataAccessError):
    return render(request, "data_access_error.html", {})


app.middleware("http")(process_unauthorized_error)
app.middleware("http")(process_forbidden_error)
