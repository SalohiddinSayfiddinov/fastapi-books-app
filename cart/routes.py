from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth.models import User
from cart.models import CartItem
from books.schemas import (
    CartAddRequest, CartUpdateRequest, CartRemoveRequest, CartResponse, CartItemResponse, BookInfo
)
from books.models import BOOKS
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/cart", tags=["cart"])

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

# --- Cart Endpoints ---
@router.post("/add", response_model=CartResponse)
def add_to_cart(request: CartAddRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Verify book exists
    book = get_book_by_id(request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    item = db.query(CartItem).filter_by(user_id=user.id, book_id=request.book_id).first()
    if item:
        item.quantity += request.quantity
    else:
        item = CartItem(user_id=user.id, book_id=request.book_id, quantity=request.quantity)
        db.add(item)
    db.commit()
    return get_cart(db, user)

@router.get("/", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(CartItem).filter_by(user_id=user.id).all()
    cart_items = []
    for item in items:
        book = get_book_by_id(item.book_id)
        if book:
            cart_items.append(CartItemResponse(
                book=BookInfo(**book.dict()),
                quantity=item.quantity
            ))
    return CartResponse(items=cart_items)

@router.post("/update", response_model=CartResponse)
def update_cart(request: CartUpdateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(CartItem).filter_by(user_id=user.id, book_id=request.book_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    item.quantity = request.quantity
    db.commit()
    return get_cart(db, user)

@router.post("/remove", response_model=CartResponse)
def remove_from_cart(request: CartRemoveRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(CartItem).filter_by(user_id=user.id, book_id=request.book_id).first()
    if item:
        db.delete(item)
        db.commit()
    return get_cart(db, user) 