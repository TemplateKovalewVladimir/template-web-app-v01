from fastapi import APIRouter, Depends
from psycopg import Cursor
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.psycopg import get_cursor
from app.db.sqlalchemy import get_async_session, get_session
from app.models.user import User

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/async")
async def hello_async(session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(text("SELECT 1 UNION SELECT 2"))
    a = [row[0] for row in res.all()]
    return {"a": a}


@router.get("/sync")
def hello_sync(session: Session = Depends(get_session)):
    q = select(User)
    s = session.execute(q)
    return 1


@router.get("/psycopg/sync")
def hello_psycopg_sync(cursor: Cursor = Depends(get_cursor)):
    cursor.execute("SELECT %(test)s as test", {"test": {"a": 12}})
    res1 = cursor.fetchone()

    return {"res1": res1}

    # cursor.execute("SELECT MAX(id) as max FROM user_account")
    # res1 = cursor.fetchone()

    # m = res1["max"] + 1
    # cursor.execute("INSERT INTO user_account VALUES (%s, %s, %s)", (m, m, m))
    # # raise Exception("test")

    # cursor.execute("SELECT MAX(id) as max FROM user_account")
    # res3 = cursor.fetchone()

    # cursor.execute("SELECT * FROM user_account")
    # res2 = cursor.fetchall()
    # return {
    #     "res1": res1,
    #     "res3": res3,
    #     "res2": res2,
    # }
