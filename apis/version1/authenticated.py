from datetime import timedelta, datetime
from typing import Union

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from starlette import status

from database import schemas, models, crud
from database.db import engine, SessionLocal
from database.schemas import User, Token

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
security = HTTPBasic()
SECRET_KEY = "b999f667097d4aaea7fa07d23b4cd8e97d24ae3fe3e0378c4cf063cc50d64121"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/documents/")
async def create_upload_file(file: bytes = File(None)):
    return {
      "doc_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
      "user_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
      "name": "string",
      "date_created": "2016-08-29T09:12:33.001Z",
      "s3_bucket_path": "string"
    }

@router.get("/documents/{doc_id}")
async def get_upload_file(doc_id: str):
    file = {}
    return file

@router.get("/documents/")
async def get_upload_file_list():
    file = {"crud.get_user()" : "111"}
    return file

@router.delete("/documents/{doc_id}", status_code=204)
async def delete_upload_file(doc_id: str):
    return

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_authenticated_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



async def verifyToken(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


@router.put("/account/{accountId}", status_code=204)
#def update_user_with_id(accountId: str, user: schemas.UserUpdate, username: str = Depends(verifyToken), db: Session = Depends(get_db)):
def update_user_with_id(accountId: str, user: schemas.UserUpdate, credentials: HTTPBasicCredentials = Depends(security),
                        db: Session = Depends(get_db)):
    result = crud.get_user_by_id(db, id=accountId)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user do not exist")
    #if result.username != username:
        #raise HTTPException(status_code=401, detail="invalid credentials for this operation")
    # alteration for basic auth
    if result.username != credentials.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not allowed",
            headers={"WWW-Authenticate": "Basic"},
        )
    current_password_bytes = bytes(credentials.password, "utf8")
    password_bytes = bytes(result.password,"utf8")
    #password_temp = b'$2b$12$TEGPvzrARipeNtouRf2Usu6mqwRySWX9dme89Dw3YkcbwHKuOjmpu'
    if not bcrypt.checkpw(current_password_bytes, password_bytes):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    #end of basic auth alteration
    result = crud.update_user(db=db, user=user, accountId=accountId)
    result_converted = User(id=result.id, first_name=result.first_name,
            last_name=result.last_name, email=result.username,
            accountCreated=result.account_created, accountupdated=result.account_updated)
    return

@router.get("/account/{accountId}", response_model=User)
#async def get_user(accountId: str, username: str = Depends(verifyToken), db: Session = Depends(get_db)):
async def get_user(accountId: str, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    result = crud.get_user_by_id(db, id=accountId)
    if not result:
        raise HTTPException(status_code=403, detail="user do not exist")
    #if result.username != username:
        #raise HTTPException(status_code=401, detail="invalid credentials for this operation")
    #alteration for basic auth
    if result.username != credentials.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not allowed",
            headers={"WWW-Authenticate": "Basic"},
        )
    current_password_bytes = bytes(credentials.password, "utf8")
    password_bytes = bytes(result.password,"utf8")
    # password_temp = b'$2b$12$TEGPvzrARipeNtouRf2Usu6mqwRySWX9dme89Dw3YkcbwHKuOjmpu'
    if not bcrypt.checkpw(current_password_bytes, password_bytes):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    #end of basic auth alteration
    result_converted = User(id=result.id, first_name=result.first_name,
                            last_name=result.last_name, email=result.username,
                            accountCreated=result.account_created, accountupdated=result.account_updated)
    return result_converted