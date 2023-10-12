from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.sqlalchemy import get_session

SessionDB = Annotated[Session, Depends(get_session)]
