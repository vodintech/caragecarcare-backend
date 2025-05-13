from fastapi import APIRouter, HTTPException
from app.database.connection import db
from bson import ObjectId
from datetime import datetime
import logging
from pydantic import BaseModel
from typing import Dict, List ,Optional

router = APIRouter()
logger = logging.getLogger(__name__)

# Response Models
class SubItem(BaseModel):
    name: str
    image: Optional[str] = None
    parts: List[str] = []
    
class ServiceItem(BaseModel):
    name: str
    subItems: List[str] = []
    subSubItems: Dict[str, List[str]] = {}

class ServiceCategory(BaseModel):
    name: str
    icon: str = ""
    items: List[ServiceItem] = []

class ServiceHierarchyResponse(BaseModel):
    _id: str
    type: str
    categories: List[ServiceCategory]
    lastUpdated: datetime = None

@router.get("/service-hierarchy")
async def get_service_hierarchy():
    try:
        hierarchy = db.service_hierarchy.find_one({"type": "service_hierarchy"})
        
        if not hierarchy:
            raise HTTPException(
                status_code=404,
                detail="Service hierarchy not found"
            )
            
        hierarchy['_id'] = str(hierarchy['_id'])
        
        # Ensure all items have required fields
        for category in hierarchy.get('categories', []):
            for item in category.get('items', []):
                item.setdefault('subItems', [])
                item.setdefault('subSubItems', {})
        
        return hierarchy
        
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch service hierarchy"
        )