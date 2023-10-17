from fastapi import APIRouter, HTTPException, status

from app import schemas
from app.services.user import UserService

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/", response_model=list[schemas.User])
def get_users():
    return UserService.get_users()


@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate):
    return UserService.create_user(user_in)


@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_in: schemas.UserUpdate):
    user = UserService.update_user(user_id, user_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int):
    user = UserService.delete_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
