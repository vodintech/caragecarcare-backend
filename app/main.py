# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes.car import router as car_router
import os
from datetime import datetime
import shutil

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create media directories if they don't exist
os.makedirs("media/brands", exist_ok=True)
os.makedirs("media/models", exist_ok=True)
os.makedirs("media/fuels", exist_ok=True)

# Serve static files
app.mount("/media", StaticFiles(directory="media"), name="media")

# Include routes
app.include_router(car_router, prefix="/car", tags=["Car"])

@app.post("/upload-brand-logo/")
async def upload_brand_logo(brand: str, file: UploadFile = File(...)):
    return await save_uploaded_file(file, "brands", brand)

@app.post("/upload-model-image/")
async def upload_model_image(brand: str, model: str, file: UploadFile = File(...)):
    return await save_uploaded_file(file, "models", f"{brand}_{model}")

@app.post("/upload-fuel-icon/")
async def upload_fuel_icon(fuel_type: str, file: UploadFile = File(...)):
    return await save_uploaded_file(file, "fuels", fuel_type)

async def save_uploaded_file(file: UploadFile, category: str, name: str):
    try:
        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_ext = file.filename.split(".")[-1]
        filename = f"{name}_{timestamp}.{file_ext}"
        filepath = f"media/{category}/{filename}"
        
        # Save the file
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename": filename, "url": f"/media/{category}/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()

@app.get("/")
def root():
    return {"status": "API is running"}