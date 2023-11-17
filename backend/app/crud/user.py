from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import UserModel
from app.schemas.user import UserCreateSchema, UserUpdateSchema


class CRUDUser(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):
    def get_user_by_username(self, db: Session, username: str) -> UserModel | None:
        return (
            db.query(self.model).filter(self.model.username == username).one_or_none()
        )


user = CRUDUser(UserModel)
