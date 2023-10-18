from pydantic import BaseModel


class UserRolesSchema(BaseModel):
    roles: list[str]


class UserBaseSchema(BaseModel):
    username: str
    surname: str
    name: str
    patronymic: str
    roles: UserRolesSchema
    avatar: str


class UserInDBBaseSchema(UserBaseSchema):
    id: int

    class Config:
        from_attributes = True


class UserSchema(UserInDBBaseSchema):
    ...


class UserCreateSchema(UserBaseSchema):
    ...


class UserUpdateSchema(UserBaseSchema):
    username: str | None = None
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    roles: UserRolesSchema | None = None
    avatar: str | None = None
