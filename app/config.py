from os import environ
from secrets import token_bytes

# Redis
REDIS_URL = environ.get("redis_url", default="redis://127.0.0.1:6379/0")


# 나이스 API Key
API_KEY = environ.get("api_key", default="#")


SECRET_KEY = token_bytes(32)
SESSION_COOKIE_NAME = "s"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
