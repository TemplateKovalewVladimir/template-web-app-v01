from enum import Enum
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Json, TypeAdapter, ValidationError, model_validator
from sqlalchemy import MetaData, Numeric, Table, create_engine, cte, desc, func, select
from sqlalchemy.orm import Session

from app.schemas import BaseModel

router = APIRouter()


sync_engine = create_engine(
    url="postgresql+psycopg://refractory:refractory@iz2vekdev:5432/refractory",
    # future=True,
    # pool_size=5,
    # max_overflow=10,
)
meta = MetaData()

r = Table("recipe", meta, autoload_with=sync_engine)
op = Table("offer_production", meta, autoload_with=sync_engine)
o = Table("offer", meta, autoload_with=sync_engine)
p = Table("people_fio", meta, autoload_with=sync_engine)
c = Table("control_mixes", meta, autoload_with=sync_engine)


class PageQuerySchema(BaseModel):
    current: int
    size: int


class PageDBSchema(BaseModel):
    limit: int
    offset: int


class SortEnum(Enum):
    ASC = "ASC"
    DESC = "DESC"


class SortQuerySchema(BaseModel):
    prop: str
    sort: SortEnum


class FilterTypeEnum(Enum):
    STRING = "string"
    NUMBER = "number"


class FilterContainsEnum(Enum):
    CONTAINS = "contains"
    NOTCONTAINS = "notcontains"


class FilterEqualsEnum(Enum):
    EQ = "eq"
    NE = "ne"


class FilterEmptyEnum(Enum):
    NULL = "null"
    NOTNULL = "notnull"


FilterStingType = FilterContainsEnum | FilterEqualsEnum | FilterEmptyEnum
FilterNumberType = FilterEqualsEnum | FilterEmptyEnum


class FilterStringSchema(BaseModel):
    type: FilterStingType
    value: str


class FilterNumberSchema(BaseModel):
    type: FilterNumberType
    value: int | float


FilterType = list[FilterStringSchema] | list[FilterNumberSchema]


class FilterQuerySchema(BaseModel):
    prop: str
    type: FilterTypeEnum
    filters: FilterType

    @model_validator(mode="after")
    def check_filters_type(self) -> "FilterQuerySchema":
        if self.type == FilterTypeEnum.NUMBER:
            for f in self.filters:
                FilterNumberSchema.model_validate(f)
        return self


FiltersQuerySchema = list[FilterQuerySchema]
FiltersQueryTypeAdapter = TypeAdapter(FiltersQuerySchema)


class QueryDBSchema(BaseModel):
    page: PageDBSchema
    sort: SortQuerySchema | None
    filters: FiltersQuerySchema | None


def json_param(param_name: str, model: type[BaseModel] | TypeAdapter, **query_kwargs):
    def get_parsed_object(value: Json = Query(alias=param_name, **query_kwargs)):
        try:
            if value is None:
                return None
            if isinstance(model, TypeAdapter):
                return model.validate_python(value)
            return model.model_validate(value)
        except ValidationError as err:
            raise HTTPException(400, detail=err.errors()) from err

    return Depends(get_parsed_object)


dep_page = json_param(
    "page",
    PageQuerySchema,
    description="Пагинация",
    openapi_examples={"Base": {"value": """{"current": 1, "size": 100}"""}},
)

dep_sort = json_param(
    "sort",
    SortQuerySchema,
    description="Сортировка",
    openapi_examples={
        "None": {"value": None},
        "Base": {"value": """{"prop": "id", "sort": "ASC"}"""},
    },
    default=None,
)

dep_filters = json_param(
    "filters",
    FiltersQueryTypeAdapter,
    description="Фильтры",
    openapi_examples={
        "None": {"value": None},
        "Base": {
            "value": """[{"prop":"control_id","type":"number","filters":[{"type":"eq","value":1}]}]"""
        },
    },
    default=None,
)


def get_query(
    page: PageQuerySchema = dep_page,
    sort: SortQuerySchema = dep_sort,
    filters: FiltersQuerySchema = dep_filters,
) -> QueryDBSchema:
    limit = page.size
    offset = page.current * page.size - page.size

    return QueryDBSchema(
        page=PageDBSchema(limit=limit, offset=offset), sort=sort, filters=filters
    )


class ListQueryParams(BaseModel):
    filter: Optional[dict[str, Any]] = Query([], description="Filters")


@router.get("/123/")
def get_data123(params: ListQueryParams = Depends()):
    return params


@router.get("/")
def get_data(query: QueryDBSchema = Depends(get_query)):
    output = []

    sort = query.sort
    offset = query.page.offset
    limit = query.page.limit

    with Session(sync_engine) as session:
        # pylint: disable=not-callable
        cte_r = cte(
            select(
                r.c,
                func.array_agg(func.DISTINCT(o.c.customer_lab)).label("customers_name"),
                func.sum(op.c.volume.cast(Numeric)).label("volume_sum"),
            )
            .select_from(r)
            .join(op, op.c.recipe_id == r.c.id)
            .join(o, o.c.id == op.c.offer_id)
            .group_by(r.c.id),
            "cte_recipe",
        )

        p_b = p.alias("p_b")
        p_m = p.alias("p_m")

        stmt = (
            (
                select(
                    c.c.id.label("control_id"),
                    c.c.date_control,
                    c.c.recipe_id,
                    c.c.sub_recipe,
                    cte_r.c.mark.label("mark"),
                    cte_r.c.alternative_mark.label("alternative_mark"),
                    cte_r.c.customers_name.label("customers_name"),
                    cte_r.c.volume_sum.label("volume_sum"),
                    c.c.work_shift,
                    c.c.mixer,
                    p_b.c.short_fio.label("brigadier"),
                    p_m.c.short_fio.label("manufacturer"),
                    c.c.trial,
                )
                .select_from(c)
                .join(cte_r, cte_r.c.id == c.c.recipe_id)
                .join(p_b, p_b.c.id == c.c.brigadier_id)
                .join(p_m, p_m.c.id == c.c.manufacturer_id)
            )
            .limit(limit)
            .offset(offset)
        )

        if sort is not None:
            if sort.sort == SortEnum.DESC:
                stmt = stmt.order_by(desc(sort.prop))
            else:
                stmt = stmt.order_by(sort.prop)

        result = session.execute(stmt)
        for row in result:
            output.append(row._asdict())

    return output
