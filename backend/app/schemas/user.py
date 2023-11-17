from enum import Enum
from typing import Annotated

from annotated_types import MaxLen

from app.schemas import BaseModel


class UserRole(Enum):
    RW = "RW"
    RO = "RO"


class UserRolesSchema(BaseModel):
    frontend: dict[str, UserRole]


class UserBaseSchema(BaseModel):
    username: Annotated[str, MaxLen(max_length=100)]
    name: Annotated[str, MaxLen(max_length=50)]
    surname: Annotated[str, MaxLen(max_length=50)]
    patronymic: Annotated[str, MaxLen(max_length=50)]
    roles: UserRolesSchema
    avatar: Annotated[str, MaxLen(max_length=100)]


class UserInDBBaseSchema(UserBaseSchema):
    id: int

    class Config:
        from_attributes = True


class UserSchema(UserInDBBaseSchema):
    ...


class UserCreateSchema(UserBaseSchema):
    ...


# class UserUpdateSchema(UserBaseSchema):
#     __annotations__ = {
#         k: Optional[v] for k, v in UserBaseSchema.__annotations__.items()
#     }


class UserUpdateSchema(UserBaseSchema):
    username: Annotated[str, MaxLen(max_length=100)] | None = None
    name: Annotated[str, MaxLen(max_length=50)] | None = None
    surname: Annotated[str, MaxLen(max_length=50)] | None = None
    patronymic: Annotated[str, MaxLen(max_length=50)] | None = None
    roles: UserRolesSchema | None = None
    avatar: Annotated[str, MaxLen(max_length=100)] | None = None
