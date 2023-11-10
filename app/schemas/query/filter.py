from datetime import date
from enum import Enum
from typing import Annotated

from annotated_types import Len
from pydantic import SkipValidation, TypeAdapter, model_validator

from app.schemas import BaseModel


class FilterTypeEnum(Enum):
    STRING = "string"
    STRING_LIST = "string[]"
    NUMBER = "number"
    DATE = "date"


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


class FilterDateEnum(Enum):
    EQ = "eq"
    BEFORE = "before"
    AFTER = "after"
    BETWEEN = "between"


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
FilterDateType = FilterDateEnum

FilterAllValueType = (
    int | float | str | date | Annotated[list[date], Len(min_length=2, max_length=2)]
)


class FilterStringSchema(BaseModel):
    type: FilterStingType
    value: str


class FilterNumberSchema(BaseModel):
    type: FilterNumberType
    value: int | float


class FilterDateSchema(BaseModel):
    type: FilterDateType
    value: date | Annotated[list[date], Len(min_length=2, max_length=2)]

    @model_validator(mode="after")
    def validator_value(self) -> "FilterDateSchema":
        if self.type == FilterDateType.BETWEEN and not isinstance(self.value, list):
            raise ValueError("The value type is not list")
        if self.type != FilterDateType.BETWEEN and not isinstance(self.value, date):
            raise ValueError("The value type is not date")

        return self


FilterSchema = FilterStringSchema | FilterNumberSchema | FilterDateSchema
FiltersType = list[FilterSchema]


class FilterQuerySchema(BaseModel):
    prop: str
    type: FilterTypeEnum
    operator: FilterOperatorEnum
    # SkipValidation нужен так как поле filters валидирую сам через validator_filters_type
    filters: SkipValidation[FiltersType]

    @model_validator(mode="after")
    def validator_filters_type(self) -> "FilterQuerySchema":
        is_type_valid = False

        if (
            self.type == FilterTypeEnum.STRING
            or self.type == FilterTypeEnum.STRING_LIST
        ):
            is_type_valid = True
            for i, f in enumerate(self.filters):
                self.filters[i] = FilterStringSchema.model_validate(f)

        if self.type == FilterTypeEnum.NUMBER:
            is_type_valid = True
            for i, f in enumerate(self.filters):
                self.filters[i] = FilterNumberSchema.model_validate(f)

        if self.type == FilterTypeEnum.DATE:
            is_type_valid = True
            for i, f in enumerate(self.filters):
                self.filters[i] = FilterDateSchema.model_validate(f)

        if not is_type_valid:
            raise ValueError(f"The type '{self.type}' is not valid")
        return self


FiltersQuerySchema = list[FilterQuerySchema]
FiltersQueryTypeAdapter = TypeAdapter(FiltersQuerySchema)
