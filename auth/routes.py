from fastapi import APIRouter, HTTPException, status, Depends
from auth.schemas import UserCreate, UserLogin, UserVerify, ForgotPasswordRequest, ResetPasswordRequest
from auth.models import User
from auth.utils import hash_password, verify_password, create_access_token, send_verification_email
from auth.database import users_db, pending_verifications
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

SUPER_OTP = "1234"

@router.post("/signup")
def signup(user: UserCreate):
    if user.email in users_db or user.email in pending_verifications:
        raise HTTPException(status_code=400, detail="Email already registered or pending verification.")
    otp = SUPER_OTP
    pending_verifications[user.email] = {"hashed_password": hash_password(user.password), "name": user.name}
    send_verification_email(user.email, otp)
    return {"msg": "Verification code sent to your email."}

@router.post("/verify")
def verify(data: UserVerify):
    if data.email not in pending_verifications:
        raise HTTPException(status_code=400, detail="No pending verification for this email.")
    if data.otp != SUPER_OTP:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    pending = pending_verifications.pop(data.email)
    user = User(id=len(users_db)+1, email=data.email, name=pending["name"], hashed_password=pending["hashed_password"], is_verified=True)
    users_db[data.email] = user
    return {"msg": "Email verified. You can now log in."}

@router.post("/login")
def login(user: UserLogin):
    db_user: Optional[User] = users_db.get(user.email)
    if not db_user or not db_user.is_verified or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials or email not verified.")
    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    if request.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found.")
    # For demo, just send the SUPER_OTP
    send_verification_email(request.email, SUPER_OTP)
    return {"msg": "Password reset OTP sent to your email."}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    if request.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found.")
    if request.otp != SUPER_OTP:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    users_db[request.email].hashed_password = hash_password(request.new_password)
    return {"msg": "Password reset successful."} 