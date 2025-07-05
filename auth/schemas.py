from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserVerify(BaseModel):
    email: EmailStr
    otp: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyPasswordResetOTP(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str 