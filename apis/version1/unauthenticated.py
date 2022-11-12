from fastapi import APIRouter


router = APIRouter()
connection = statsd.Connection(
       host='127.0.0.1',
       port=8125,
       sample_rate=1,
   )
client = statsd.Client("python", connection)
counter = client.get_counter("counter")

@router.get("/")
def hello():
    counter += 1
    return {"message": "Hello World"}
