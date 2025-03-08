import os
from fastapi import APIRouter
from .controllers import healthcheck, authentication, users
router = APIRouter()

#Define custom routes controller. 
router.include_router(healthcheck.router)
router.include_router(authentication.router)
router.include_router(users.router)