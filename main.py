from starlette.staticfiles import StaticFiles

from auth.middleware import process_unauthorized_error, process_forbidden_error
from routers import catalog_controller, cart_controller
from auth.router import router as auth_router
from settings import STATIC_ROOT, STATIC_URL, MEDIA_ROOT, MEDIA_URL
from app import app


app.include_router(catalog_controller.router)
app.include_router(cart_controller.router)
app.include_router(auth_router)
app.mount(STATIC_URL, StaticFiles(directory=STATIC_ROOT), name="static")
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name="media")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.middleware("http")(process_unauthorized_error)
app.middleware("http")(process_forbidden_error)
