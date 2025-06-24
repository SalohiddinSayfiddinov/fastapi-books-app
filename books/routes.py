from fastapi import APIRouter, Query
from .models import BOOKS
from typing import List, Optional

router = APIRouter()

@router.get("/books")
def list_books():
    return BOOKS

@router.get("/books/search")
def search_books(
    q: Optional[str] = Query(None, description="Search term for title, author, or category")
) -> List[dict]:
    if not q:
        return BOOKS
    q_lower = q.lower()
    return [
        book for book in BOOKS
        if q_lower in book.title.lower() or q_lower in book.author.lower() or q_lower in book.category.lower()
    ] 