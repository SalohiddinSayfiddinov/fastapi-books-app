from fastapi import APIRouter, Query
from .models import BOOKS


router = APIRouter(tags=["books"])

@router.get("/books")
def get_books():
    return BOOKS

@router.get("/books/{book_id}")
def get_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}

@router.get("/search/")
def search_books(q: str = Query(..., description="Search query")):
    results = []
    for book in BOOKS:
        if q.lower() in book.title.lower() or q.lower() in book.author.lower():
            results.append(book)
    return results

@router.get("/category/{category}")
def get_books_by_category(category: str):
    results = []
    for book in BOOKS:
        if book.category.lower() == category.lower():
            results.append(book)
    return results

@router.get("/author/{author}")
def get_books_by_author(author: str):
    results = []
    for book in BOOKS:
        if book.author.lower() == author.lower():
            results.append(book)
    return results

@router.get("/top-of-week/")
def get_top_of_week_books():
    return [book for book in BOOKS if book.top_of_week]
