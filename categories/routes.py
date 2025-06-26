from fastapi import APIRouter
from .models import CATEGORIES

router = APIRouter(tags=['categories'])

@router.get("/categories")
def list_categories():
    return CATEGORIES 