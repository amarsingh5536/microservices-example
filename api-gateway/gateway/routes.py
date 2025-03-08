import os
from fastapi import APIRouter
from .controllers import authentication
router = APIRouter()

#Define custom routes controller. 
router.include_router(authentication.router)