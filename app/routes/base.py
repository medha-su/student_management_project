from fastapi import APIRouter
from app.routes.create_student import router as create_router
from app.routes.get_student import router as get_router
from app.routes.update_student import router as update_router
from app.routes.delete_student import router as delete_router
from app.routes.ai_query import router as ai_router

api_router = APIRouter()
api_router.include_router(create_router, tags=["Students"])
api_router.include_router(get_router, tags=["Students"])
api_router.include_router(update_router, tags=["Students"])
api_router.include_router(delete_router, tags=["Students"])
api_router.include_router(ai_router, tags=["Optional Local AI"])
