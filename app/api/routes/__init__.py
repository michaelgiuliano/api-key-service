from fastapi import APIRouter
from app.api.routes import auth, api_keys


router = APIRouter()
router.include_router(auth.router)
router.include_router(api_keys.router)
