from fastapi import FastAPI

from .api.endpoints import api_v1_router
from .core.config import Settings, get_settings

settings: Settings = get_settings()

app: FastAPI = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, description=settings.APP_DESCRIPTION, debug=settings.DEBUG
)

app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
