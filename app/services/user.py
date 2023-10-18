from app import crud
from app.middleware.db import get_session
from app.models.user import UserModel
from app.schemas.user import UserCreateSchema, UserUpdateSchema


def get_user(user_id: int) -> UserModel | None:
    db = get_session()
    return crud.user.get(db, user_id)


def get_users() -> list[UserModel]:
    db = get_session()
    return crud.user.get_multi(db)


def create_user(user_in: UserCreateSchema) -> UserModel:
    db = get_session()
    new_user = crud.user.create(db, obj_in=user_in)
    db.commit()
    return new_user


def update_user(user_id: int, user_in: UserUpdateSchema) -> UserModel | None:
    db = get_session()
    user = crud.user.get(db, id=user_id)
    if not user:
        return None
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    db.commit()
    return user


def delete_user(user_id: int) -> UserModel | None:
    db = get_session()
    user = crud.user.get(db, id=user_id)
    if not user:
        return None
    user = crud.user.remove(db, id=user_id)
    db.commit()
    return user
