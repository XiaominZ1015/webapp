
from fastapi import APIRouter

from apis.version1 import public, unauthenticated, authenticated

api_router = APIRouter()
api_router.include_router(public.router, prefix="/v1", tags=["public"])
api_router.include_router(unauthenticated.router, prefix="/healthz", tags=["unauthenticated"])
api_router.include_router(authenticated.router, prefix="/v1", tags=["authenticated"])
