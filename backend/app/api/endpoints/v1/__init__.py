from fastapi import APIRouter

from .base import base_router

api_v1_router: APIRouter = APIRouter()

api_v1_router.include_router(base_router)
