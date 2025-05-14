from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes.car import router as car_router
from app.config import settings
from app.routes.service import router as service_router
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://caragecarcare.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Create media directories if they don't exist
os.makedirs(settings.MEDIA_ROOT / "brands", exist_ok=True)
os.makedirs(settings.MEDIA_ROOT / "models", exist_ok=True)
os.makedirs(settings.MEDIA_ROOT / "fuels", exist_ok=True)

# Serve static files
app.mount(
    str(settings.MEDIA_URL),
    StaticFiles(directory=settings.MEDIA_ROOT),
    name="media"
)

# Include routes
app.include_router(car_router, prefix="/car", tags=["Car"])

@app.get("/")
def root():
    return {"status": "API is running"}

logger.info(f"📁 Media root: {settings.MEDIA_ROOT}")
logger.info(f"🌐 Media URL: {settings.MEDIA_URL}")

app.include_router(service_router)
@app.get("/")
def read_root():
    return {"message": "Service Hierarchy API is running"}