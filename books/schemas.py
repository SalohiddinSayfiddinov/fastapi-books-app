from pydantic import BaseModel
from typing import List, Optional

class CartAddRequest(BaseModel):
    book_id: int
    quantity: int = 1

class CartUpdateRequest(BaseModel):
    book_id: int
    quantity: int

class CartRemoveRequest(BaseModel):
    book_id: int

class BookInfo(BaseModel):
    id: int
    title: str
    price: float
    image: str
    description: str
    author: str
    category: str
    rating: float
    review_count: int
    publisher: str
    published_date: str
    language: str
    page_count: int
    isbn: str
    vendor: str
    special_offer: bool
    stock_status: str
    offer: bool = False
    discount: Optional[int] = 0
    top_of_week: bool = False

class CartItemResponse(BaseModel):
    book: BookInfo
    quantity: int

class CartResponse(BaseModel):
    items: List[CartItemResponse]

class WishlistAddRequest(BaseModel):
    book_id: int

class WishlistRemoveRequest(BaseModel):
    book_id: int

class WishlistItemResponse(BaseModel):
    book: BookInfo

class WishlistResponse(BaseModel):
    items: List[WishlistItemResponse] 