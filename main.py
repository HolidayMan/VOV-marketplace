from fastapi import FastAPI
from routers import catalog_controller

app = FastAPI()
app.include_router(catalog_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
