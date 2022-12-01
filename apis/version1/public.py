import json
import os
import time
import boto3
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
import logging
import statsd
from starlette import status

from database import schemas, models, crud
from database.db import engine, SessionLocal
from database.schemas import User
from boto3.dynamodb.conditions import Key

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
statsd = statsd.StatsClient(host='127.0.0.1',
                     port=8125,
                     prefix="public")
SECRET_KEY = "b999f667097d4aaea7fa07d23b4cd8e97d24ae3fe3e0378c4cf063cc50d64121"
ALGORITHM = "HS256"

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_onetime_token(email: str):
    payload = {
      "email":""
    }
    payload["email"] = email
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

    token = create_onetime_token(result.username)
    # publish message
    sns_client = boto3.client("sns", region_name="us-east-1")
    SNSTopic = os.getenv('topic')
    email = str(result.username)
    url0 = ",http://sherryzxm.com/v1/verifyUserEmail/"
    url1 = url0 + email + "/"
    url2 = url1 + str(token)
    message = email + url2
    response = sns_client.publish(
        TopicArn=SNSTopic,
        Message=message
    )

    # insert into DynamoDB table
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    ttl = int(time.time()) + 120
    dynamodb.Table('csye6225').put_item(
        Item={
            "email": result.username,
            "token": token,
            "ttl": ttl
        }
    )
    foo_timer.stop()
    return result_converted

@router.get("/verifyUserEmail/{email}/{token}")
def verify_email(email: str, token: str, db: Session = Depends(get_db)):
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    response = dynamodb.Table('csye6225').get_item(
        Key={'email': email}
    )
    item = response['Item']
    if item['token'] == token and item['ttl'] > int(time.time()):
        db_user = crud.get_user_by_email(db, email=email)
        user = schemas.UserUpdate(verify=1)
        # json_raw = '{"verify": 1}'
        # user_dict = json.loads(json_raw)
        # user = schemas.UserBase(**user_dict)
        crud.update_user(db=db, user=user, accountId=db_user.id)
        return {"message": "account verified"}
    elif item['ttl'] <= int(time.time()):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="verify link expired",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invaild token",
            headers={"WWW-Authenticate": "Basic"},
        )