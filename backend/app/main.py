"""
AI Logistics Platform - Main Application
National Transport Hackathon 2026
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from app.core.config import get_settings
from app.core.database import engine, Base

# Import routers
from app.api.v1.endpoints import orders, vehicles, matching, routing

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    AI-powered logistics platform for Uzbekistan's E-Logistika system.
    
    ## Features
    
    * **Smart Matching** - AI подбор транспорта для груза
    * **Cargo Safety Checker** - AI проверка безопасности груза (ADR, фитосанитарные сертификаты)
    * **AI Route Validator** - Построение маршрутов с учётом ограничений для грузов
    * **Document Management** - Управление ЭТТН, путевыми листами, сертификатами
    * **Permit Management** - Управление рухсатнома (международные разрешения)
    * **Telegram Mini App** - Мобильный интерфейс для водителей
    
    ## Integrations
    
    * Yandex Maps & Routing API (Hackathon Partner)
    * OpenWeatherMap API (погода на маршруте)
    * OpenRouteService API (ограничения для грузовиков)
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}ms"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": time.time()
    }


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AI Logistics Platform API",
        "docs": "/docs",
        "version": settings.APP_VERSION
    }


# Include routers
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["vehicles"])
app.include_router(matching.router, prefix="/api/v1/matching", tags=["ai-matching"])
app.include_router(routing.router, prefix="/api/v1/routing", tags=["ai-routing"])


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("Database tables created")
    logger.info("Services initialized")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
