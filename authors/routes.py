from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from .models import AUTHORS, Author
from books.models import BOOKS

router = APIRouter()

@router.get("/authors", response_model=List[Author])
def list_authors():
    return AUTHORS

@router.get("/authors/{author_id}", response_model=Author)
def get_author(author_id: int):
    author = next((a for a in AUTHORS if a.id == author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.get("/authors/search/by_name")
def search_authors(
    q: Optional[str] = Query(None, description="Search term for author name or nationality"),
    genre: Optional[str] = Query(None, description="Filter by genre")
):
    results = AUTHORS
    
    if q:
        q_lower = q.lower()
        results = [
            author for author in results
            if q_lower in author.name.lower() or q_lower in author.nationality.lower()
        ]
    
    if genre:
        genre_lower = genre.lower()
        results = [
            author for author in results
            if any(g.lower() == genre_lower for g in author.genres)
        ]
    
    return results

@router.get("/authors/{author_id}/books")
def get_author_books(author_id: int):
    author = next((a for a in AUTHORS if a.id == author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    author_books = [
        book for book in BOOKS
        if book.author == author.name
    ]
    
    return author_books 