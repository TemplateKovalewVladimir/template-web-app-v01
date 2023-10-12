from fastapi import APIRouter, HTTPException, status

from app import crud, schemas
from app.api.dependencies import SessionDB

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: SessionDB):
    user = crud.user.get(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return user


@router.get("/", response_model=list[schemas.User])
def get_users(db: SessionDB):
    return crud.user.get_multi(db)


@router.post("/", response_model=schemas.User)
def create_user(db: SessionDB, user_in: schemas.UserCreate):
    new_user = crud.user.create(db, obj_in=user_in)
    db.commit()
    return new_user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(db: SessionDB, user_id: int, user_in: schemas.UserUpdate):
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    db.commit()
    return user


@router.delete("/{id}", response_model=schemas.User)
def delete_user(db: SessionDB, id: int):
    item = crud.user.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.user.remove(db=db, id=id)
    db.commit()
    return item
