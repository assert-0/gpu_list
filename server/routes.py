from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
async def get_index() -> list:
    RedirectResponse(url="/static/index.html")


@router.get("/index.html")
async def get_index_html() -> list:
    RedirectResponse(url="/static/index.html")


