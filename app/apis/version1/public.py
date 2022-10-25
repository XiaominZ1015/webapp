from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import models, crud, schemas
from app.database.db import engine, SessionLocal
from app.database.schemas import User
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/account", response_model=User)
def create_account(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    result = crud.create_user(db=db, user=user)
    result_converted = User(id=result.id, first_name=result.first_name,
            last_name=result.last_name, email=result.username,
            accountCreated=result.account_created, accountupdated=result.account_updated)
    return result_converted