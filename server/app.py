from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import index_router
from .v2.routes import api_v2_router
from .v3.routes import api_v3_router

app = FastAPI()
app.include_router(index_router)
app.include_router(api_v2_router)
app.include_router(api_v3_router)
app.mount("/static", StaticFiles(directory="."), name="static")
