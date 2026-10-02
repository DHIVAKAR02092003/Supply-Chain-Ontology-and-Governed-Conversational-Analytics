from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.api.routes import health, personas, ontology, ai
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Supply Chain Analytics API",
    description="Persona-based supply chain analytics backed by Snowflake",
    version="1.0.0",
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(personas.router)
app.include_router(ontology.router)
app.include_router(ai.router)

# Serve React build if available (single-container deployment)
# Check multiple possible locations (local dev vs Docker)
_candidates = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist"),
    "/app/frontend/dist",
]
for _path in _candidates:
    if os.path.exists(_path):
        app.mount("/", StaticFiles(directory=_path, html=True), name="frontend")
        break
