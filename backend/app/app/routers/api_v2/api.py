import logging

from fastapi import APIRouter, Security

from app.routers.api_v2.endpoints import login, users, utils, api_key, farms
from app.routers.api_v2.endpoints.resources import resources
from app.routers.utils.security import get_farm_access, get_current_active_superuser

logger = logging.getLogger(__name__)

router = APIRouter()
router.include_router(login.router, tags=["login"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(utils.router, prefix="/utils", tags=["utils"])

# Include /api-keys endpoint, require superuser to access.
router.include_router(
    api_key.router,
    prefix="/api-keys",
    tags=["api keys"],
    dependencies=[Security(get_current_active_superuser)]
)

# Include /farms endpoints.
router.include_router(
    farms.router,
    prefix="/farms",
    tags=["farms"],
)

# Include /farms/logs endpoints.
router.include_router(
    resources.router,
    prefix="/farms/resources",
    tags=["Resources"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.logs'])]
)