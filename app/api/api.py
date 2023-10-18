from fastapi import APIRouter, Depends

from app.api.dependencies import current_user_depends
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
    dependencies=[Depends(current_user_depends)],
)
