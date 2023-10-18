from pydantic import BaseModel


class TokenSchema(BaseModel):
    token: str


class TokenPayloadBaseSchema(BaseModel):
    create: float
    exp: float


class TokenUserPayloadSchema(BaseModel):
    username: str


class TokenPayloadSchema(TokenPayloadBaseSchema, TokenUserPayloadSchema):
    ...
