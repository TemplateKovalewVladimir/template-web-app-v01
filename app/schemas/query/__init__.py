from fastapi import Depends, HTTPException, Query
from pydantic import Json, TypeAdapter, ValidationError

from app.schemas import BaseModel
from app.schemas.query.filter import FiltersQuerySchema, FiltersQueryTypeAdapter
from app.schemas.query.page import PageDBSchema, PageQuerySchema
from app.schemas.query.sort import SortQuerySchema


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
