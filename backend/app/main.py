from fastapi import FastAPI

from .core.config import Settings, get_settings
from .core.security import *

settings: Settings = get_settings()

app: FastAPI = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, description=settings.APP_DESCRIPTION)
