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

def get_sns_topic():
    sns_topic = os.getenv('topic')
    sns_topic = sns_topic[13:]
    return sns_topic


def create_onetime_token(email: str):
    to_encode = email.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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
    #publish message
    sns_client = boto3.client("sns", regin_name="us-east-1")
    topic_arn = get_sns_topic()
    message = result.username
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
    )['MessageId']
    # insert into DynamoDB table
    dynamodb = boto3.client('dynamodb')
    token = create_onetime_token(result.username)
    dynamodb.Table('csye6225').put_item(
        Item={
            "email": {"S": result.username},
            "token": {"S": token}}
    )
    return result_converted

@router.post("/verifyUserEmail/{email}{token}", status_code=204)
def verify_email(email: str, token: str, db: Session = Depends(get_db)):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.Table('csye6225').query(
        KeyConditionExpression=Key('email').eq(email)
    )
    if(response.token == token):
        db_user = crud.get_user_by_email(db, email=email)
        json_raw = '{"verify": 1}'
        user_dict = json.loads(json_raw)
        user = schemas.UserUpdate(**user_dict)
        crud.update_user(db=db, user=user, accountId=db_user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invaild token",
            headers={"WWW-Authenticate": "Basic"},
        )
