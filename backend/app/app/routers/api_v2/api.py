import logging

from fastapi import APIRouter, Security

from app.routers.api_v2.endpoints import login, users, utils, api_key
from app.routers.utils.security import get_current_active_superuser

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
