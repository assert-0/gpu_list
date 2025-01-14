from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from . import consts


config = Config('.env')
auth = OAuth(config)

auth.register(
    "auth0",
    client_id=consts.AUTH0_CLIENT_ID,
    client_secret=consts.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=consts.AUTH_SERVER_METADATA_URL,
)
