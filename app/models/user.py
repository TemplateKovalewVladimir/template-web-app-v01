from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.schemas.user import UserRoles

AVATAR_DEFAULT = "default.gif"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    patronymic: Mapped[str] = mapped_column(String(50))
    roles: Mapped[UserRoles] = mapped_column(type_=JSONB)
    avatar: Mapped[str] = mapped_column(
        String(100),
        default=AVATAR_DEFAULT,
        server_default=AVATAR_DEFAULT,
    )

    def __str__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

    def __repr__(self) -> str:
        return self.__str__()
