from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from database import Base

class OrderStatus(str, enum.Enum):
    pending = "pending"
    on_the_way = "on_the_way"
    delivered = "delivered"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    datetime = Column(String, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    book_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    order = relationship("Order", back_populates="items") 