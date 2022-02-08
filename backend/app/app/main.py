import logging

from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.core.config import settings
from app.routers import api_v2

# Configure logging. Change INFO to DEBUG for development logging.
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.AGGREGATOR_NAME,
    description="farmOS Aggregator Backend",
    version="v0.9.5",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(api_v2.router, prefix=settings.API_V2_PREFIX)
