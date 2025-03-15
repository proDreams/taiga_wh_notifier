from fastapi import APIRouter

from src.presentation.web_app_routes.update_route import update_router
from src.presentation.web_app_routes.webhook_route import webhook_router

web_app_router = APIRouter()

web_app_router.include_router(update_router)
web_app_router.include_router(webhook_router)
