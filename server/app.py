from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import index_router, api_router

app = FastAPI()
app.include_router(index_router)
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="."), name="static")
