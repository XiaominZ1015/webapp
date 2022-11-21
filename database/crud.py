from datetime import datetime

import bcrypt as bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.username == email).first()

def get_user_by_id(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_authenticated_user(db: Session, userName: str, password: str):
    user = db.query(models.User).filter(models.User.username == userName).first()
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return user


def create_user(db: Session, user: schemas.UserCreate):
    passwordInBytes = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(passwordInBytes, salt)
    password_str = password.decode('utf-8')
    db_user = models.User(
        first_name=user.first_name, last_name=user.last_name,
        username=user.username, password=password_str,
        account_created=datetime.now(), account_updated=datetime.now(), verify=0
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate, accountId: str):
    userFound = get_user_by_id(db, id=accountId)
    if not userFound:
        raise HTTPException(status_code=404, detail="user do not exist")
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == 'passward':
            passwordInBytes = value.encode('utf-8')
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(passwordInBytes, salt)
            setattr(userFound, key, password)
        setattr(userFound, key, value)
    setattr(userFound, 'account_updated', datetime.now())
    db.add(userFound)
    db.commit()
    db.refresh(userFound)
    return userFound
