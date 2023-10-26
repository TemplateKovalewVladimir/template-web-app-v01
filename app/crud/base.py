from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelTypeT = TypeVar("ModelTypeT", bound=Base)
CreateSchemaTypeT = TypeVar("CreateSchemaTypeT", bound=BaseModel)
UpdateSchemaTypeT = TypeVar("UpdateSchemaTypeT", bound=BaseModel)


# python 3.12 -> class CRUDBase[ModelTypeT, CreateSchemaTypeT, UpdateSchemaTypeT]:
class CRUDBase(Generic[ModelTypeT, CreateSchemaTypeT, UpdateSchemaTypeT]):
    def __init__(self, model: Type[ModelTypeT]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelTypeT]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, order_by: Any = None, skip: int = 0, limit: int = 100
    ) -> List[ModelTypeT]:
        return db.query(self.model).order_by(order_by).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaTypeT) -> ModelTypeT:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        # Если к db_obj будет обращение после commit, то будет отправлен запрос к БД
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelTypeT,
        obj_in: UpdateSchemaTypeT,
    ) -> ModelTypeT:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                # jsonable_encoder нужен, если update_data[field] сложный объект
                setattr(db_obj, field, jsonable_encoder(update_data[field]))
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        # Если к db_obj будет обращение после commit, то будет отправлен запрос к БД
        return db_obj

    # pylint: disable-next=W0622
    def remove(self, db: Session, *, id: int) -> ModelTypeT:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.flush()
        return obj
