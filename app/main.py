from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import os

def create_application() -> FastAPI:

    app = FastAPI(
        title="Tech Trend Tracker API",
        description="API for analyzing technology trends",
        version="1.0.0"
    )

    # CORS configuration
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router, prefix="/api")

    return app

app = create_application()