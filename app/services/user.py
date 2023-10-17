from app import crud, schemas
from app.middleware.db import get_session
from app.models.user import User


class UserService:
    @staticmethod
    def get_user(user_id: int) -> User | None:
        db = get_session()
        return crud.user.get(db, user_id)

    @staticmethod
    def get_users() -> list[User]:
        db = get_session()
        return crud.user.get_multi(db)

    @staticmethod
    def create_user(user_in: schemas.UserCreate) -> User:
        db = get_session()
        new_user = crud.user.create(db, obj_in=user_in)
        db.commit()
        return new_user

    @staticmethod
    def update_user(user_id: int, user_in: schemas.UserUpdate) -> User | None:
        db = get_session()
        user = crud.user.get(db, id=user_id)
        if not user:
            return None
        user = crud.user.update(db, db_obj=user, obj_in=user_in)
        db.commit()
        return user

    @staticmethod
    def delete_user(user_id: int) -> User | None:
        db = get_session()
        user = crud.user.get(db, id=user_id)
        if not user:
            return None
        user = crud.user.remove(db, id=user_id)
        db.commit()
        return user
