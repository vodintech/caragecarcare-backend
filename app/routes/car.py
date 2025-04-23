# app/routes/car.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.database.connection import db
from app.models.car import CarBrand, CarRequest
from typing import List
import os

router = APIRouter()  # Changed from car_router to router

@router.get("/brand-logos", response_model=List[dict])
async def get_brand_logos():
    logos = []
    try:
        for filename in os.listdir("media/brands"):
            if not filename.startswith("."):
                brand_name = filename.split("_")[0]
                logos.append({
                    "brand": brand_name,
                    "url": f"/media/brands/{filename}"
                })
        return logos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-images/{brand}", response_model=List[dict])
async def get_model_images(brand: str):
    images = []
    try:
        for filename in os.listdir("media/models"):
            if filename.startswith(f"{brand}_") and not filename.startswith("."):
                parts = filename.split("_")
                model_name = "_".join(parts[1:-1])
                images.append({
                    "model": model_name,
                    "url": f"/media/models/{filename}"
                })
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fuel-icons", response_model=List[dict])
async def get_fuel_icons():
    icons = []
    try:
        for filename in os.listdir("media/fuels"):
            if not filename.startswith("."):
                fuel_type = filename.split("_")[0]
                icons.append({
                    "type": fuel_type,
                    "url": f"/media/fuels/{filename}"
                })
        return icons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Existing routes
@router.post("/add-brand", response_model=CarBrand)
async def add_car_brand(data: CarBrand):
    if db.brands.find_one({"brand": data.brand}):
        raise HTTPException(status_code=400, detail="Brand already exists")
    
    result = db.brands.insert_one(data.dict())
    inserted = db.brands.find_one({"_id": result.inserted_id}, {"_id": 0})
    return inserted

@router.get("/all-brands", response_model=List[CarBrand])
async def get_all_brands():
    brands = list(db.brands.find({}, {"_id": 0}))
    return brands

@router.get("/get-models/{brand_name}", response_model=CarBrand)
async def get_models_by_brand(brand_name: str):
    brand_data = db.brands.find_one({"brand": brand_name}, {"_id": 0})
    if not brand_data:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand_data

@router.post("/submit-request")
async def submit_car_request(request: CarRequest):
    try:
        db.requests.insert_one(request.dict())
        return {"message": "Request submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))