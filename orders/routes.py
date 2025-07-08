from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from orders.models import Order, OrderItem, OrderStatus
from .schemas import OrderCreate, OrderRead, OrderStatusUpdate
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from cart.models import CartItem
from auth.models import User

router = APIRouter(tags=["orders"])

# --- Authentication Dependency (copied from cart/routes.py) ---
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

@router.post("/orders", response_model=OrderRead)
def create_order(order: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Fetch user's cart items
    cart_items = db.query(CartItem).filter_by(user_id=user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    db_order = Order(
        user_id=user.id,
        latitude=order.latitude,
        longitude=order.longitude,
        datetime=order.datetime,
        status=OrderStatus.pending
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # Create order items
    for item in cart_items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            book_id=item.book_id,
            quantity=item.quantity
        )
        db.add(db_order_item)
    # Clear user's cart
    db.query(CartItem).filter_by(user_id=user.id).delete()
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders", response_model=list[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all() 

@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order