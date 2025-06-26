from fastapi import APIRouter, Query
from .models import BOOKS
from typing import List, Optional

router = APIRouter(tags=["books"])

@router.get("/books")
def list_books(
    search: Optional[str] = Query(None, description="Search by title or author"),
    category: Optional[str] = Query(None, description="Filter by category name. Novels, Science, History, Biography, Fantasy")
):
    results = BOOKS

    if search:
        search_lower = search.lower()
        results = [
            book for book in results
            if search_lower in book.title.lower() or search_lower in book.author.lower()
        ]

    if category:
        category_lower = category.lower()
        results = [
            book for book in results
            if book.category.lower() == category_lower
        ]

    return results

@router.get("/books/offers")
def get_offer_books():
    return [book for book in BOOKS if book.offer]


@router.get("/books/top")
def get_top_of_week_books():
    return [book for book in BOOKS if book.top_of_week]
