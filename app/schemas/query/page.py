from app.schemas import BaseModel


class PageQuerySchema(BaseModel):
    current: int
    size: int


class PageDBSchema(BaseModel):
    limit: int
    offset: int
