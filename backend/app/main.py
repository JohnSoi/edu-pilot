from fastapi import FastAPI
from .core import get_settings, Settings

settings: Settings = get_settings()

app: FastAPI = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, description=settings.APP_DESCRIPTION)
