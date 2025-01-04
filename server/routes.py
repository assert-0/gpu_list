from fastapi import APIRouter
from fastapi.responses import RedirectResponse

index_router = APIRouter(prefix="")


@index_router.get("/")
async def get_index() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")


@index_router.get("/index.html")
async def get_index_html() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")
