from sqlalchemy import MetaData, Numeric, Table, and_, create_engine, select
from sqlalchemy.orm import Session, aliased

# Sync
sync_engine = create_engine(
    url="postgresql+psycopg://expenses:expenses@iz2vekdev:5432/expenses",
    echo=True,
    # future=True,
    # pool_size=5,
    # max_overflow=10,
)

meta = MetaData()
# meta.reflect(sync_engine)

expense = Table("expense", meta, autoload_with=sync_engine)
people = Table("people", meta, autoload_with=sync_engine)

with Session(sync_engine) as session:
    columns = ()

    people1 = aliased(people, "people1")
    people2 = aliased(people, "people2")

    column_sum = expense.c.receipts["sum"].cast(Numeric).label("sum")

    stmt = (
        select(
            expense.c.id,
            people1.c.name.label("people_peo"),
            people2.c.name.label("people_re"),
            column_sum,
        )
        .select_from(expense)
        .join(people1, expense.c.people_peo == people1.c.id)
        .join(people2, expense.c.people_re == people2.c.id)
        .where(
            and_(
                expense.c.id >= 1,
                expense.c.id >= 2,
                column_sum > 2,
            )
        )
        .limit(10)
    )

    result = session.execute(stmt)

    for row in result:
        print(row)

    print(stmt)


with Session(sync_engine) as session:
    insert = expense.insert().values(
        category="123",
        people_peo=1,
        people_re=1,
        contract_aa=1,
        contract_contractor=1,
        contractor=1,
        product_name=1,
        cash=1,
        currency=1,
        date_contract=1,
        invoices=1,
        receipts=1,
        payments_percent=1,
        receipts_percent=1,
        payments_residual=1,
        receipts_residual=1,
    )

    result = session.execute(insert)

    session.commit()

    print(insert)
