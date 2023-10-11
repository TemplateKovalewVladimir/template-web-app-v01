from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas
from app.db.sqlalchemy import get_session
from app.models.user import User

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    return session.query(User).filter(User.id == user_id).first()


@router.get("/", response_model=list[schemas.User])
def get_users(session: Session = Depends(get_session)):
    return session.query(User).order_by(User.id).all()


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    session: Session = Depends(get_session),
    user_in: schemas.UserCreate,
):
    obj_in_data = jsonable_encoder(user_in)
    db_obj = User(**obj_in_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
