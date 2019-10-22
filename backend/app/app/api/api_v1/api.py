from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils
from app.api.api_v1.endpoints.farms import farms, logs, assets, terms, areas

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

api_router.include_router(farms.router,  prefix="/farms", tags=["farms"])
api_router.include_router(logs.router, prefix="/farms/logs", tags=["farm logs"])
api_router.include_router(assets.router, prefix="/farms/assets", tags=["farm assets"])
api_router.include_router(terms.router, prefix="/farms/terms", tags=["farm terms"])
api_router.include_router(areas.router, prefix="/farms/areas", tags=["farm areas"])
