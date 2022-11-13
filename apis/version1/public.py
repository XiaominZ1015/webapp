import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import statsd
from database import schemas, models, crud
from database.db import engine, SessionLocal
from database.schemas import User
models.Base.metadata.create_all(bind=engine)

router = APIRouter()
statsd = statsd.StatsClient(host='127.0.0.1',
                     port=8125,
                     prefix="public")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/account", response_model=User)
def create_account(user: schemas.UserCreate, db: Session = Depends(get_db)):
    statsd.incr('create_account')
    logging.info("user creating a account")

    foo_timer = statsd.timer('create_account_timer')
    foo_timer.start()

    db_user = crud.get_user_by_email(db, email=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    result = crud.create_user(db=db, user=user)
    result_converted = User(id=result.id, first_name=result.first_name,
            last_name=result.last_name, username=result.username,
            accountCreated=result.account_created, accountupdated=result.account_updated)
    foo_timer.stop()
    return result_converted