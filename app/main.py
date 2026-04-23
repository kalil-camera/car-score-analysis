"""
Main FastAPI application
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api import router as vehicles_router
from app.config import settings
from app.database import create_tables, get_db
from app.models import DataCollectionLog
from app.schemas import HealthResponse
from app.workers import run_all_workers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown"""
    # Startup
    logger.info("Starting up application...")
    create_tables()
    logger.info("Database tables created/verified")

    # Run workers on startup (optional)
    try:
        logger.info("Running initial data workers...")
        await run_all_workers()
        logger.info("Initial workers completed")
    except Exception as e:
        logger.error(f"Error running workers: {e}")

    yield

    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
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
app.include_router(vehicles_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        db_status = "unhealthy"

    # Get recent worker status
    recent_logs = db.query(DataCollectionLog).order_by(
        DataCollectionLog.created_at.desc()
    ).limit(3).all()

    workers_status = {
        log.worker_name: log.status for log in recent_logs
    }

    return HealthResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        version=settings.api_version,
        timestamp=datetime.utcnow(),
        database=db_status,
        workers=workers_status,
    )


@app.get("/workers/logs", tags=["workers"])
async def get_worker_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Get recent worker execution logs"""
    logs = db.query(DataCollectionLog).order_by(
        DataCollectionLog.created_at.desc()
    ).limit(limit).all()

    return [
        {
            "id": log.id,
            "worker": log.worker_name,
            "status": log.status,
            "processed": log.items_processed,
            "failed": log.items_failed,
            "start": log.start_time,
            "end": log.end_time,
            "timestamp": log.created_at,
        }
        for log in logs
    ]


@app.post("/workers/run", tags=["workers"])
async def trigger_workers():
    """Manually trigger workers"""
    try:
        await run_all_workers()
        return {
            "status": "success",
            "message": "Workers executed successfully",
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error(f"Error running workers: {e}")
        return {
            "status": "failed",
            "message": str(e),
            "timestamp": datetime.utcnow(),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
