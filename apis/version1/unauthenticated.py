
from fastapi import APIRouter
from statsd.defaults.env import statsd

router = APIRouter()

@router.get("/")
def hello():
    statsd.incr("sss")
    return {"message": "Hello World"}
