from apis.version1 import public
from apis.version1 import unauthenticated
from apis.version1 import authenticated
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(public.router, prefix="/V0", tags=["public"])
api_router.include_router(unauthenticated.router, prefix="/healthz", tags=["unauthenticated"])
api_router.include_router(authenticated.router, prefix="/users", tags=["authenticated"])