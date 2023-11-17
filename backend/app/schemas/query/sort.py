from enum import Enum

from app.schemas import BaseModel


class SortEnum(Enum):
    ASC = "ASC"
    DESC = "DESC"


class SortQuerySchema(BaseModel):
    prop: str
    sort: SortEnum
