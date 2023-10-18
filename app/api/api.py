from fastapi import APIRouter

from app.api.dependencies import X_API_KEY_DEPENDS
from app.api.endpoints import login, user

api_router = APIRouter()

api_router.include_router(
    login.router,
    prefix="/login",
    tags=["login"],
)
api_router.include_router(
    user.router,
    prefix="/users",
    tags=["user"],
    dependencies=[X_API_KEY_DEPENDS],
)
