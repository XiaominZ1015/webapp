from fastapi import APIRouter
import statsd
router = APIRouter()
statsd = statsd.StatsClient(host='127.0.0.1',
                     port=8125,
                     prefix="unauthenticated")

@router.get("/", status_code=204)
def hello():
    statsd.incr('hello')
    return {"message": "Hello Change"}
