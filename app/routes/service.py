from fastapi import APIRouter, HTTPException
from app.database.connection import db
from fastapi.responses import JSONResponse
from bson import ObjectId
from datetime import datetime
import logging
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()
logger = logging.getLogger(__name__)

# Response Models
class Part(BaseModel):
    name: str
    image: Optional[str] = None

class SubItem(BaseModel):
    name: str
    image: Optional[str] = None
    parts: List[Part] = []

class ServiceItem(BaseModel):
    name: str
    image: Optional[str] = None
    subItems: List[SubItem] = []

class ServiceCategory(BaseModel):
    name: str
    icon: str
    items: List[ServiceItem] = []

class ServiceHierarchyResponse(BaseModel):
    categories: List[ServiceCategory]
    lastUpdated: datetime

@router.get("/service-hierarchy")
async def get_service_hierarchy():
    try:
        # Get all category documents
        categories = list(db.service_hierarchy.find({"type": "service_category"}))
        
        if not categories:
            logger.warning("No service categories found in database")
            return JSONResponse(
                status_code=200,
                content={
                    "categories": [],
                    "lastUpdated": datetime.utcnow().isoformat()
                }
            )
            
        # Convert ObjectId to string for JSON serialization
        for category in categories:
            category["_id"] = str(category["_id"])
            for item in category.get("items", []):
                for subItem in item.get("subItems", []):
                    for part in subItem.get("parts", []):
                        if "_id" in part:
                            part["_id"] = str(part["_id"])

        return {
            "categories": categories,
            "lastUpdated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Database error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)  # Return the actual error message for debugging
        )