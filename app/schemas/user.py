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


class UserCreate(UserBase):
    ...


class User(UserInDBBase):
    ...
