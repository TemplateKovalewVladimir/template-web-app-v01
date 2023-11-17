from fastapi import APIRouter
from sqlalchemy import MetaData, Numeric, Table, create_engine, cte, func, select
from sqlalchemy.orm import Session

from app.api.dependencies import QueryPaginateSortFiltersDepends
from app.db.query import process_query_filters

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


@router.get("/")
def get_data(query: QueryPaginateSortFiltersDepends):
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

        stmt = process_query_filters(query, stmt)

        return session.execute(stmt).mappings().all()
