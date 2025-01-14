from typing import Union

from authlib.oauth2 import OAuth2Error
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from ..utils import auth

api_auth_router = APIRouter(prefix="/api/auth")


@api_auth_router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    return await auth.auth0.authorize_redirect(
        request, redirect_uri=redirect_uri, _external=True
    )

@api_auth_router.get("/callback", response_model=None)
async def callback(request: Request) -> Union[RedirectResponse, HTMLResponse]:
    try:
        token = await auth.auth0.authorize_access_token(request)
    except OAuth2Error as error:
        return HTMLResponse(
            f"<h1>Authentication failed</h1>"
            f"<p>{error.description}</p>"
        )
    if token:
        request.session['user'] = token
    return RedirectResponse(url='/')

@api_auth_router.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.pop('user', None)
    return RedirectResponse(url='/')

    # Disabled for lab4

    # return RedirectResponse(
    #     consts.AUTH_LOGOUT_URL
    #     + "?"
    #     + urlencode(
    #         {
    #             "returnTo": request.url_for("get_index"),
    #             "client_id": consts.AUTH0_CLIENT_ID,
    #         },
    #         quote_via=quote_plus,
    #     )
    # )
