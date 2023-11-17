from contextvars import ContextVar

from fastapi import Request
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.sqlalchemy import session_maker
from app.middleware.exception import SessionNotInitialisedError

db: ContextVar[Session | None] = ContextVar("db", default=None)


def get_session() -> Session:
    session = db.get()
    if session is None:
        raise SessionNotInitialisedError()
    return db.get()


class MiddlewareDB(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        with session_maker() as session:
            token = db.set(session)
            response = await call_next(request)
            db.reset(token)
            return response
