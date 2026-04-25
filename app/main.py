"""Main FastAPI application - Clean Architecture entry point"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import create_tables, get_db
from app.container import initialize_container
from app.presentation import (
    vehicle_router,
    price_router,
    safety_router,
    reliability_router,
)
from app.application import HealthResponse
from app.infrastructure.persistence.orm_models import DataCollectionLogORM

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    logger.info("🚀 Starting application...")
    create_tables()
    logger.info("✅ Database initialized")
    
    # Initialize DI Container
    initialize_container(get_db)
    logger.info("✅ DI Container initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vehicle_router)
app.include_router(price_router)
app.include_router(safety_router)
app.include_router(reliability_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "environment": settings.environment,
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        db_status = "unhealthy"
    
    # Get recent worker executions
    recent_logs = db.query(DataCollectionLogORM).order_by(
        DataCollectionLogORM.created_at.desc()
    ).limit(3).all()
    
    workers_status = {}
    for log in recent_logs:
        if log.worker_name not in workers_status:
            workers_status[log.worker_name] = log.status
    
    return HealthResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        version=settings.api_version,
        timestamp=datetime.utcnow(),
        database=db_status,
        workers=workers_status,
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
