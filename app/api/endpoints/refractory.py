import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import (
    ForeignKey,
    MetaData,
    Numeric,
    Select,
    Table,
    and_,
    column,
    create_engine,
    cte,
    desc,
    func,
    or_,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from app.schemas.query import QueryDBSchema, get_query
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

router = APIRouter()


sync_engine = create_engine(
    url="postgresql+psycopg://refractory:refractory@iz2vekdev:5432/refractory",
    # future=True,
    # pool_size=5,
    # max_overflow=10,
)

# Императивный
meta = MetaData()

r = Table("recipe", meta, autoload_with=sync_engine)
op = Table("offer_production", meta, autoload_with=sync_engine)
o = Table("offer", meta, autoload_with=sync_engine)
p = Table("people_fio", meta, autoload_with=sync_engine)
c = Table("control_mixes", meta, autoload_with=sync_engine)


# Декларативный
class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark: Mapped[str]
    alternative_mark: Mapped[str]
    offer_productions: Mapped["OfferProduction"] = relationship(back_populates="recipe")


class OfferProduction(Base):
    __tablename__ = "offer_production"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))
    offer_id: Mapped[int] = mapped_column(ForeignKey("offer.id"))
    volume: Mapped[float]
    recipe: Mapped["Recipe"] = relationship(back_populates="offer_productions")


class Offer(Base):
    __tablename__ = "offer"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_lab: Mapped[str]


class ControlMixes(Base):
    __tablename__ = "control_mixes"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_control: Mapped[datetime.date]
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))
    sub_recipe: Mapped[str]
    work_shift: Mapped[str]
    mixer: Mapped[str]
    brigadier_id: Mapped[int] = mapped_column(ForeignKey("people_fio.id"))
    brigadier = relationship("PeopleFio", foreign_keys=[brigadier_id])
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("people_fio.id"))
    manufacturer: Mapped["PeopleFio"] = relationship(foreign_keys=[manufacturer_id])
    trial: Mapped[int]


class PeopleFio(Base):
    __tablename__ = "people_fio"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_fio: Mapped[str]


@router.get("/123/")
def get_data123():
    with Session(sync_engine) as session:
        # # pylint: disable=not-callable
        # cte_recipe = (
        #     select(
        #         Recipe,
        #         func.array_agg(func.DISTINCT(Offer.customer_lab)).label(
        #             "customers_name"
        #         ),
        #         func.sum(cast(OfferProduction.volume, Float)).label("volume_sum"),
        #     )
        #     .join(OfferProduction, Recipe.id == OfferProduction.recipe_id)
        #     .join(Offer, OfferProduction.offer_id == Offer.id)
        #     .group_by(Recipe.id)
        #     .cte("cte_recipe")
        # )

        # people_brigadier = aliased(PeopleFio)
        # people_manufacturer = aliased(PeopleFio)

        # query = select(
        #     select(
        #         ControlMixes.id.label("control_id"),
        #         ControlMixes.date_control,
        #         ControlMixes.recipe_id,
        #         ControlMixes.sub_recipe,
        #         cte_recipe.c.mark,
        #         cte_recipe.c.alternative_mark,
        #         cte_recipe.c.customers_name,
        #         cte_recipe.c.volume_sum,
        #         ControlMixes.work_shift,
        #         ControlMixes.mixer,
        #         people_brigadier.short_fio.label("brigadier"),
        #         people_manufacturer.short_fio.label("manufacturer"),
        #         ControlMixes.trial,
        #     )
        #     .join(cte_recipe, ControlMixes.recipe_id == cte_recipe.c.id)
        #     .join(
        #         people_brigadier,
        #         ControlMixes.brigadier_id == people_brigadier.id,
        #     )
        #     .join(
        #         people_manufacturer,
        #         ControlMixes.manufacturer_id == people_manufacturer.id,
        #     )
        #     .cte("cte")
        # ).where(column("control_id") == 16530)

        # result = session.execute(query)

        # return result.mappings().all()

        # ------------

        stmt = session.query(Recipe).where(column("id") == 9057).limit(10)
        return stmt.all()

        # ------------

        # stmt = select(RecipeModel.id).limit(10)
        # result = session.execute(stmt)
        # return [row._asdict() for row in result]


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


@router.get("/")
def get_data(query: QueryDBSchema = Depends(get_query)):
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

        stmt = cte(
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
            .join(p_m, p_m.c.id == c.c.manufacturer_id),
            "cte",
        )
        stmt = select(stmt)

        stmt = query_paginate(stmt, query.page.limit, query.page.offset)
        if query.sort is not None:
            stmt = query_sort(stmt, query.sort)
        if query.filters is not None:
            stmt = query_filters(stmt, query.filters)

        return session.execute(stmt).mappings().all()
