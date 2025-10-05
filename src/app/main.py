from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
from .config import settings
from .api import routers
from .models.database import create_tables
import os

# Configure logging
logger = structlog.get_logger()

def create_application() -> FastAPI:
    app = FastAPI(
        title="Drive-Thru Ordering System",
        description="AI-powered restaurant ordering assistant",
        version="1.0.0",
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(routers.api_router, prefix="/api/v1")

    return app

app = create_application()

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("drive_thru_system_starting", environment=settings.ENVIRONMENT)

    # Create database tables
    if settings.CREATE_TABLES:
        create_tables()
        logger.info("database_tables_created")

    # Initialize services
    await initialize_services()

    logger.info("drive_thru_system_started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("drive_thru_system_shutting_down")

async def initialize_services():
    """Initialize all required services"""
    # Initialize LLM service
    from .services.llm_service import LLMService
    app.state.llm_service = LLMService()

    # Initialize order service
    from .services.order_service import OrderService
    app.state.order_service = OrderService()

    logger.info("services_initialized")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "drive-thru-ordering",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        workers=1 if settings.ENVIRONMENT == "development" else 4
    )