from typing import Any

from psycopg.cursor import BaseCursor, Cursor
from psycopg.rows import DictRow, RowMaker, dict_row
from psycopg.types.json import JsonbDumper
from psycopg_pool import ConnectionPool

from app.core.config import settings

pool = ConnectionPool(
    settings.database_url_psycopg3,
    min_size=4,
    open=True,
    # TODO: date style
    # kwargs={"options": "-c datestyle=ISO,YMD"},
)


def my_dict_row(cursor: BaseCursor[Any, Any]) -> RowMaker[DictRow]:
    print(cursor._query.query.decode())
    print(cursor._query.params)
    return dict_row(cursor)


def get_cursor() -> Cursor:
    with pool.connection() as conn:
        # Register dumper
        conn.adapters.register_dumper(dict, JsonbDumper)

        # Create cursor
        with conn.cursor(row_factory=my_dict_row) as cursor:
            try:
                print("---start---")
                yield cursor
            except Exception:
                print("---exception---")
                conn.rollback()
            else:
                print("---commit---")
                conn.commit()
            finally:
                print("---end---")
