"""
Real-Time Patient Monitoring System - FastAPI Application Entry Point
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

from app.config import settings
from app.api import patients, metrics, websocket_handlers
from app.database import init_db, engine
from sqlalchemy import text
from app.redis_client import redis_client

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)
PATIENT_OPERATIONS = Counter(
    'patient_operations_total',
    'Total patient operations',
    ['operation', 'status']
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown
    """
    # Startup
    logger.info("Starting Patient Monitoring System...")
    try:
        await init_db()
        await redis_client.connect()
        logger.info("Database and Redis initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Patient Monitoring System...")
    try:
        await redis_client.disconnect()
        logger.info("Services shut down successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="Real-Time Patient Monitoring System",
    description="Scalable, cloud-native patient monitoring platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routes
app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(websocket_handlers.router, prefix="/ws", tags=["websocket"])


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for Kubernetes liveness/readiness probes
    """
    try:
        # Check database connectivity
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        
        # Check Redis connectivity
        await redis_client.ping()
        
        return {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": __import__("datetime").datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


# Metrics endpoint for Prometheus
@app.get("/metrics", tags=["monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint
    """
    return Response(content=generate_latest(), media_type="text/plain")


# Root endpoint
@app.get("/", tags=["info"])
async def root():
    """
    API information endpoint
    """
    return {
        "name": "Real-Time Patient Monitoring System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
