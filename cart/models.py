from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer)
    quantity = Column(Integer, default=1)

    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='_user_book_cart_uc'),)
