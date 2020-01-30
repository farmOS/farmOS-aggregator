import logging

from fastapi import APIRouter, Depends, Security

from app.core import config
from app.api.api_v1.endpoints import login, users, utils
from app.api.api_v1.endpoints.farms import farms, info, logs, assets, terms, areas
from app.api.utils.security import get_farm_access

logger = logging.getLogger(__name__)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

# Include /farms endpoints.
api_router.include_router(
    farms.router,
    prefix="/farms",
    tags=["farms"],
)

# Include /farms/info endpoint.
api_router.include_router(
    info.router,
    prefix="/farms/info",
    tags=["farm info"],
)

# Include /farms/logs endpoints.
api_router.include_router(
    logs.router,
    prefix="/farms/logs",
    tags=["farm logs"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.logs'])]
)

# Include /farms/assets endpoints.
api_router.include_router(
    assets.router,
    prefix="/farms/assets",
    tags=["farm assets"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.assets'])]
)

# Include /farms/terms endpoints.
api_router.include_router(
    terms.router,
    prefix="/farms/terms",
    tags=["farm terms"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.terms'])]
)

# Include /farms/areas endpoints.
api_router.include_router(
    areas.router,
    prefix="/farms/areas",
    tags=["farm areas"],
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.areas'])]
)
