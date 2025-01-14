from environs import Env

env = Env()
env.read_env()


AUTH0_CLIENT_ID = env.str("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = env.str("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = env.str("AUTH0_DOMAIN")
APP_SECRET_KEY = env.str("APP_SECRET_KEY")

AUTH_SERVER_METADATA_URL = f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration"
AUTH_LOGOUT_URL = f"https://{AUTH0_DOMAIN}/v2/logout"

TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
