from pydantic import BaseModel, Field
from typing import List
from orders.models import OrderStatus

class OrderCreate(BaseModel):
    latitude: float
    longitude: float
    datetime: str  # e.g., '07-07-2025 17:00'

class OrderItemRead(BaseModel):
    id: int
    book_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    user_id: int
    latitude: float
    longitude: float
    datetime: str
    status: OrderStatus  
    items: List[OrderItemRead]

    class Config:
        orm_mode = True
        use_enum_values = True 

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

    model_config = {
        "use_enum_values": True,
        "from_attributes": True
    }