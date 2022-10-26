from apis.version1 import unauthenticated, authenticated, public
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(public.router, prefix="/v1", tags=["public"])
api_router.include_router(unauthenticated.router, prefix="/healthz", tags=["unauthenticated"])
api_router.include_router(authenticated.router, prefix="/v1/account", tags=["authenticated"])