from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import catalog_controller
from settings import STATIC_ROOT, STATIC_URL


app = FastAPI()
app.include_router(catalog_controller.router)
app.mount(STATIC_URL, StaticFiles(directory=STATIC_ROOT), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}
