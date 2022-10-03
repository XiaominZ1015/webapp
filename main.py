from apis.base import api_router
from fastapi import FastAPI



def include_router(app):
    app.include_router(api_router)



def start_application():
    app = FastAPI()
    include_router(app)
    return app


app = start_application()

