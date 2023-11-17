from sqlalchemy import Select, and_, column, desc, func, or_

from app.schemas.query import QueryDBSchema
from app.schemas.query.filter import (
    FilterAllType,
    FilterAllValueType,
    FilterCompareEnum,
    FilterCompareEqualsEnum,
    FilterContainsEnum,
    FilterDateEnum,
    FilterEmptyEnum,
    FilterEqualsEnum,
    FilterOperatorEnum,
    FiltersQuerySchema,
    FilterTypeEnum,
)
from app.schemas.query.sort import SortEnum, SortQuerySchema


def query_sort(stmt: Select, sort: SortQuerySchema):
    columns_name = stmt.exported_columns.keys()
    column_name = sort.prop
    if column_name not in columns_name:
        raise ValueError(f"Sort prop '{column_name}' does not exist")

    if sort.sort == SortEnum.ASC:
        return stmt.order_by(column_name)
    if sort.sort == SortEnum.DESC:
        return stmt.order_by(desc(column_name))
    return stmt


def get_expression(
    column_name: str,
    column_type: FilterTypeEnum,
    filter_type: FilterAllType,
    value: FilterAllValueType,
):
    _column = column(column_name)

    if column_type == FilterTypeEnum.STRING:
        # Contains
        if filter_type == FilterContainsEnum.CONTAINS:
            return _column.ilike(f"%{value}%")
        if filter_type == FilterContainsEnum.NOTCONTAINS:
            return _column.notilike(f"%{value}%")

        # Equals
        if filter_type == FilterEqualsEnum.EQ:
            return _column == value
        if filter_type == FilterEqualsEnum.NE:
            return _column != value

        # Empty
        if filter_type == FilterEmptyEnum.NULL:
            return _column.is_(None)
        if filter_type == FilterEmptyEnum.NOTNULL:
            return _column.is_not(None)

    if column_type == FilterTypeEnum.STRING_LIST:
        # Contains
        if filter_type == FilterContainsEnum.CONTAINS:
            return func.array_to_string(_column, " ").ilike(f"%{value}%")
        if filter_type == FilterContainsEnum.NOTCONTAINS:
            return func.array_to_string(_column, " ").notilike(f"%{value}%")

    if column_type == FilterTypeEnum.NUMBER:
        # Equals
        if filter_type == FilterEqualsEnum.EQ:
            return _column == value
        if filter_type == FilterEqualsEnum.NE:
            return _column != value

        # Compare
        if filter_type == FilterCompareEnum.GT:
            return _column > value
        if filter_type == FilterCompareEnum.LT:
            return _column < value

        # CompareEquals
        if filter_type == FilterCompareEqualsEnum.GE:
            return _column >= value
        if filter_type == FilterCompareEqualsEnum.LE:
            return _column <= value

        # Empty
        if filter_type == FilterEmptyEnum.NULL:
            return _column.is_(None)
        if filter_type == FilterEmptyEnum.NOTNULL:
            return _column.is_not(None)

    if column_type == FilterTypeEnum.DATE:
        # Date
        if filter_type == FilterDateEnum.EQ:
            return _column == value
        if filter_type == FilterDateEnum.BEFORE:
            return _column <= value
        if filter_type == FilterDateEnum.AFTER:
            return _column >= value
        if filter_type == FilterDateEnum.BETWEEN:
            return _column.between(value[0], value[1])

    raise NotImplementedError(
        f"Type filter '{filter_type}' and type column '{column_type}' not implemented"
    )


def query_filters(stmt: Select, filters: FiltersQuerySchema):
    columns_name = stmt.exported_columns.keys()

    for f in filters:
        column_name = f.prop
        column_type = f.type

        if column_name not in columns_name:
            raise ValueError(f"Filter prop '{column_name}' does not exist")

        expressions = [
            get_expression(column_name, column_type, _f.type, _f.value)
            for _f in f.filters
        ]

        if f.operator == FilterOperatorEnum.OR:
            stmt = stmt.where(or_(*expressions))
        if f.operator == FilterOperatorEnum.AND:
            stmt = stmt.where(and_(*expressions))

    return stmt


def query_paginate(stmt: Select, limit: int, offset: int):
    stmt = stmt.limit(limit)
    stmt = stmt.offset(offset)
    return stmt


def process_query_filters(query: QueryDBSchema, stmt: Select):
    stmt = stmt.cte("cte").select()

    stmt = query_paginate(stmt, query.page.limit, query.page.offset)
    if query.sort is not None:
        stmt = query_sort(stmt, query.sort)
    if query.filters is not None:
        stmt = query_filters(stmt, query.filters)
    return stmt
