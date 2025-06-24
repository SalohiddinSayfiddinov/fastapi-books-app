from fastapi import APIRouter
from .models import CATEGORIES

router = APIRouter()

@router.get("/categories")
def list_categories():
    return CATEGORIES 