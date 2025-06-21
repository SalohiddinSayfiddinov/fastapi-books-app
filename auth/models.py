from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    is_verified: bool = False 