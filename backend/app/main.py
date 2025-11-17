"""
MediSense-AI FastAPI Application Entry Point.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime

from app.core.config import settings
from app.core.logger import get_logger, setup_logging
from app.db import init_db
from app.api.v1 import routes_auth, routes_agents, routes_mcp

# Initialize logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting MediSense-AI application", version="1.0.0", env=settings.ENV)

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")

    yield

    # Shutdown
    logger.info("Shutting down MediSense-AI application")


# Create FastAPI application
app = FastAPI(
    title="MediSense-AI",
    description="Enterprise Clinical AI Multi-Agent Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred",
            "path": request.url.path
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "running",
            "database": "connected",  # Would check actual DB connection
            "redis": "connected",  # Would check actual Redis connection
            "mcp": settings.MCP_MODE
        }
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MediSense-AI",
        "description": "Enterprise Clinical AI Multi-Agent Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(routes_agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(routes_mcp.router, prefix="/api/v1/mcp", tags=["MCP"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
