from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str

# Hardcoded categories
CATEGORIES = [
    Category(id=1, name="Novels"),
    Category(id=2, name="Science"),
    Category(id=3, name="History"),
    Category(id=4, name="Biography"),
    Category(id=5, name="Fantasy"),
] 