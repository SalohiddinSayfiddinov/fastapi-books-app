from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth.models import User
from wishlist.models import WishlistItem
from books.schemas import (
    WishlistAddRequest, WishlistRemoveRequest, WishlistResponse, WishlistItemResponse, BookInfo
)
from books.models import BOOKS
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

def get_book_by_id(book_id: int):
    """Helper function to get book by ID from the BOOKS list"""
    for book in BOOKS:
        if book.id == book_id:
            return book
    return None

# --- Authentication Dependency ---
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Wishlist Endpoints ---
@router.post("/add", response_model=WishlistResponse)
def add_to_wishlist(request: WishlistAddRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Verify book exists
    book = get_book_by_id(request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    item = db.query(WishlistItem).filter_by(user_id=user.id, book_id=request.book_id).first()
    if not item:
        item = WishlistItem(user_id=user.id, book_id=request.book_id)
        db.add(item)
        db.commit()
    return get_wishlist(db, user)

@router.get("/", response_model=WishlistResponse)
def get_wishlist(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(WishlistItem).filter_by(user_id=user.id).all()
    wishlist_items = []
    for item in items:
        book = get_book_by_id(item.book_id)
        if book:
            wishlist_items.append(WishlistItemResponse(
                book=BookInfo(**book.dict())
            ))
    return WishlistResponse(items=wishlist_items)

@router.post("/remove", response_model=WishlistResponse)
def remove_from_wishlist(request: WishlistRemoveRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(WishlistItem).filter_by(user_id=user.id, book_id=request.book_id).first()
    if item:
        db.delete(item)
        db.commit()
    return get_wishlist(db, user) 