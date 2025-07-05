from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from database import Base

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer)

    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='_user_book_wishlist_uc'),) 