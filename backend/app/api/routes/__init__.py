from fastapi import APIRouter
from app.api.routes.user import router as user_router
from app.api.routes.data_type import router as data_type_router
from app.api.routes.calculate import router as calculate_router
from app.api.routes.correlation import router as correlation_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(data_type_router, prefix="/data_type", tags=["data_type"])
router.include_router(calculate_router, prefix="/calculate", tags=["user"])
router.include_router(correlation_router, prefix="/correlation", tags=["user"])
