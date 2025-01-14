from typing import Union

from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from .consts import TEMPLATES_DIR, STATIC_DIR
from .v2.util import export_csv, export_json
from ..tools.model import GPUModel

index_router = APIRouter(prefix="")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@index_router.get("/")
async def get_index() -> RedirectResponse:
    return RedirectResponse(url="/index.html")


@index_router.get("/index.html")
async def get_index_html(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        name="index.html.jinja2",
        request=request,
        context={
            "is_authenticated": "user" in request.session,
            "user": request.session.get("user", None),
        },
    )


@index_router.get("/user-profile.html", response_model=None)
async def get_user_profile_html(
        request: Request, response: Response
) -> Union[HTMLResponse, RedirectResponse]:
    if not request.session.get("user", None):
        response.status_code = 403
        return RedirectResponse(url="/static/login-required.html")

    return templates.TemplateResponse(
        name="user-profile.html.jinja2",
        request=request,
        context={
            "is_authenticated": "user" in request.session,
            "user": request.session.get("user", None),
        },
    )


@index_router.get("/refresh-copies")
async def refresh_copies(
        request: Request, response: Response
) -> RedirectResponse:
    if not request.session.get("user", None):
        response.status_code = 403
        return RedirectResponse(url="/static/login-required.html")

    csv_dump = export_csv(GPUModel.filter())
    json_dump = export_json(GPUModel.filter())

    with open(f"{STATIC_DIR}/gpu_models.csv", "w") as f:
        f.write(csv_dump)

    with open(f"{STATIC_DIR}/gpu_models.json", "w") as f:
        f.write(json_dump)

    return RedirectResponse(url="/static/copies-refreshed.html")
