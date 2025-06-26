from fastapi import APIRouter, Query
from typing import Optional
from .models import VENDORS, VENDOR_CATEGORIES

router = APIRouter(tags=["vendors"])

@router.get("/vendors")
def get_vendors(category: Optional[str] = Query(None, description="Filter by vendor category")):
    if category and category.lower() != "all":
        return [vendor for vendor in VENDORS if vendor.category.lower() == category.lower()]
    return VENDORS

@router.get("/vendor-categories")
def get_vendor_categories():
    return VENDOR_CATEGORIES
