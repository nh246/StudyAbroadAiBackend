from fastapi import APIRouter
from api.v1.endpoints.profile import router as profile_router
from api.v1.endpoints.chat import router as chat_router

router = APIRouter()

router.include_router(profile_router)
router.include_router(chat_router)

__all__ = ["router"]