from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema
from app.services import UserService

router = APIRouter()


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/", response_model=list[UserSchema])
def get_users():
    return UserService.get_users()


@router.post("/", response_model=UserSchema)
def create_user(user_in: UserCreateSchema):
    return UserService.create_user(user_in)


@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_in: UserUpdateSchema):
    user = UserService.update_user(user_id, user_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(user_id: int):
    user = UserService.delete_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
