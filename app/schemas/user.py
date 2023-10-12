from typing import Optional

from pydantic import BaseModel


class UserRoles(BaseModel):
    roles: list[str]


class UserBase(BaseModel):
    username: str
    surname: str
    patronymic: str
    roles: UserRoles
    avatar: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True


class User(UserInDBBase):
    ...


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    username: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    roles: UserRoles | None = None
    avatar: str | None = None
