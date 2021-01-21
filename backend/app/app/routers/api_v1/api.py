import logging

from fastapi import APIRouter, Depends, Security

from app.routers.api_v1.endpoints import login, users, utils, api_key
from app.routers.api_v1.endpoints.farms import farms, info, logs, assets, terms, areas
from app.routers.utils.security import get_farm_access, get_current_active_superuser

logger = logging.getLogger(__name__)

router = APIRouter()
router.include_router(login.router, tags=["login"], deprecated=True)
router.include_router(users.router, prefix="/users", tags=["users"], deprecated=True)
router.include_router(utils.router, prefix="/utils", tags=["utils"], deprecated=True)

# Include /api-keys endpoint, require superuser to access.
router.include_router(
    api_key.router,
    prefix="/api-keys",
    tags=["api keys"],
    dependencies=[Security(get_current_active_superuser)],
    deprecated=True
)

# Include /farms endpoints.
router.include_router(
    farms.router,
    prefix="/farms",
    tags=["farms"],
)

# Include /farms/info endpoint.
router.include_router(
    info.router,
    prefix="/farms/info",
    tags=["farm info"],
)

# Include /farms/logs endpoints.
router.include_router(
    logs.router,
    prefix="/farms/logs",
    tags=["farm logs"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.logs'])]
)

# Include /farms/assets endpoints.
router.include_router(
    assets.router,
    prefix="/farms/assets",
    tags=["farm assets"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.assets'])]
)

# Include /farms/terms endpoints.
router.include_router(
    terms.router,
    prefix="/farms/terms",
    tags=["farm terms"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.terms'])]
)

# Include /farms/areas endpoints.
router.include_router(
    areas.router,
    prefix="/farms/areas",
    tags=["farm areas"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.areas'])]
)
