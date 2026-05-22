from fastapi import APIRouter, Depends

from app.api.middleware.auth_checker import verify_token
from app.api.router.health.route_health import health_router
from app.api.router.auth.auth_route import auth_router
from app.api.router.cv.route_cv import cv_router

api_router = APIRouter()


# --- Public Routes ---------------------------------
public_routers = [health_router, auth_router]
for router in public_routers:
    api_router.include_router(router)


# --- Protected Routes ---------------------------
protected_router = APIRouter(dependencies=[Depends(verify_token)])
protected_routers = [cv_router]
for router in protected_routers:
    protected_router.include_router(router)

api_router.include_router(protected_router)
