from enum import Enum

from pydantic import TypeAdapter, model_validator

from app.schemas import BaseModel


class FilterTypeEnum(Enum):
    STRING = "string"
    STRING_LIST = "string[]"
    NUMBER = "number"


class FilterOperatorEnum(Enum):
    OR = "or"
    AND = "and"


class FilterContainsEnum(Enum):
    CONTAINS = "contains"
    NOTCONTAINS = "notcontains"


class FilterEqualsEnum(Enum):
    EQ = "eq"
    NE = "ne"


class FilterCompareEnum(Enum):
    GT = "gt"
    LT = "lt"


class FilterCompareEqualsEnum(Enum):
    GE = "ge"
    LE = "le"


class FilterEmptyEnum(Enum):
    NULL = "null"
    NOTNULL = "notnull"


FilterAllType = (
    FilterContainsEnum
    | FilterEqualsEnum
    | FilterCompareEnum
    | FilterCompareEqualsEnum
    | FilterEmptyEnum
)
FilterStingType = FilterContainsEnum | FilterEqualsEnum | FilterEmptyEnum
FilterNumberType = (
    FilterEqualsEnum | FilterCompareEnum | FilterCompareEqualsEnum | FilterEmptyEnum
)

FilterAllValueType = int | float | str


class FilterStringSchema(BaseModel):
    type: FilterStingType
    value: str


class FilterNumberSchema(BaseModel):
    type: FilterNumberType
    value: int | float


FilterSchema = FilterStringSchema | FilterNumberSchema
FiltersType = list[FilterSchema]


class FilterQuerySchema(BaseModel):
    prop: str
    type: FilterTypeEnum
    operator: FilterOperatorEnum
    filters: FiltersType

    @model_validator(mode="after")
    def check_filters_type(self) -> "FilterQuerySchema":
        if self.type == FilterTypeEnum.NUMBER:
            for f in self.filters:
                FilterNumberSchema.model_validate(f)
        return self


FiltersQuerySchema = list[FilterQuerySchema]
FiltersQueryTypeAdapter = TypeAdapter(FiltersQuerySchema)
