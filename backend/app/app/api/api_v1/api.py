from fastapi import APIRouter, Depends

from app.api.api_v1.endpoints import login, users, utils
from app.api.api_v1.endpoints.farms import farms, logs, assets, terms, areas
from app.api.utils.security import get_current_user

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

# Include /farms endpoints.
api_router.include_router(
    farms.router,
    prefix="/farms",
    tags=["farms"],
    dependencies=[Depends(get_current_user)]
)

# Include /farms/logs endpoints.
api_router.include_router(
    logs.router,
    prefix="/farms/logs",
    tags=["farm logs"],
    dependencies=[Depends(get_current_user)]
)

# Include /farms/assets endpoints.
api_router.include_router(
    assets.router,
    prefix="/farms/assets",
    tags=["farm assets"],
    dependencies=[Depends(get_current_user)]
)

# Include /farms/terms endpoints.
api_router.include_router(
    terms.router,
    prefix="/farms/terms",
    tags=["farm terms"],
    dependencies=[Depends(get_current_user)]
)

# Include /farms/areas endpoints.
api_router.include_router(
    areas.router,
    prefix="/farms/areas",
    tags=["farm areas"],
    dependencies=[Depends(get_current_user)]
)
