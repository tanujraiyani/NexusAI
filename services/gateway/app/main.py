from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import app.db.base
from app.api.v1.router import router as api_v1_router
from app.common.exceptions import (
    AlreadyExistsException,
    ForbiddenException,
    NexusAIException,
    NotFoundException,
    UnauthorizedException,
)
from app.common.middleware.request_id import RequestIDMiddleware
from app.common.responses import error_response
from app.core.logger import logger, setup_logger
from app.db.database import Base, engine

setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting NexusAI Gateway...")
    logger.info(f"Registered models: {list(Base.metadata.tables.keys())}")
    logger.info("Database schema is managed by Alembic.")
    yield
    logger.info("Shutting down NexusAI Gateway...")


app = FastAPI(
    title="NexusAI Gateway",
    version="1.0.0",
    description="API Gateway for NexusAI",
    lifespan=lifespan,
)

# --------------------------------------------------
# Middleware
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestIDMiddleware)

# --------------------------------------------------
# Exception Handlers
# --------------------------------------------------


@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(
    request: Request,
    exc: AlreadyExistsException,
):
    return error_response(
        message=exc.message,
        status_code=409,
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(
    request: Request,
    exc: UnauthorizedException,
):
    return error_response(
        message=exc.message,
        status_code=401,
    )


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(
    request: Request,
    exc: ForbiddenException,
):
    return error_response(
        message=exc.message,
        status_code=403,
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException,
):
    return error_response(
        message=exc.message,
        status_code=404,
    )


@app.exception_handler(NexusAIException)
async def nexus_exception_handler(
    request: Request,
    exc: NexusAIException,
):
    return error_response(
        message=exc.message,
        status_code=400,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception("Unhandled exception occurred")

    return error_response(
        message="Internal Server Error",
        status_code=500,
    )


# --------------------------------------------------
# Routes
# --------------------------------------------------

logger.info("Gateway starting...")

app.include_router(api_v1_router)


@app.get("/")
async def root():
    logger.info("Root endpoint called")

    return {
        "success": True,
        "message": "Welcome to NexusAI Gateway",
        "version": "1.0.0",
    }