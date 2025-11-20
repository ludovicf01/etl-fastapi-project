"""main"""
from typing import Union

from fastapi import FastAPI


from app.config import settings
from .routers import etl
from .routers import upload

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Routes
app.include_router(upload.router)
app.include_router(etl.router)


@app.get("/")
def read_root():
    """test"""
    return {"msg": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """test 2"""
    return {"item_id": item_id, "q": q}
