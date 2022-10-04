from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import models, schemas, crud
from database.db import engine, SessionLocal
from database.schemas import User
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{accountId}", response_model=User)
def get_user_by_id(accountId: str, db: Session = Depends(get_db)):
    result = crud.get_user_by_id(db, id=accountId)
    if not result:
        raise HTTPException(status_code=404, detail="user do not exist")
    result_converted = User(id=result.id, first_name=result.first_name,
            last_name=result.last_name, email=result.username,
            accountCreated=result.account_created, accountupdated=result.account_updated)
    return result_converted

@router.put("/{accountId}", response_model=User)
def update_user_with_id(accountId: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):

    result = crud.update_user(db=db, user=user, accountId=accountId)
    result_converted = User(id=result.id, first_name=result.first_name,
            last_name=result.last_name, email=result.username,
            accountCreated=result.account_created, accountupdated=result.account_updated)
    return result_converted