from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .consts import STATIC_DIR
from .routes import index_router
from .auth.routes import api_auth_router
from .v2.routes import api_v2_router
from .v3.routes import api_v3_router

app = FastAPI()
app.include_router(index_router)
app.include_router(api_auth_router)
app.include_router(api_v2_router)
app.include_router(api_v3_router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.add_middleware(SessionMiddleware, secret_key="!secret")
