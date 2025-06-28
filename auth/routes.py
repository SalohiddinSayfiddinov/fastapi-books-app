from fastapi import APIRouter, HTTPException, status, Depends
from auth.schemas import UserCreate, UserLogin, UserVerify, ForgotPasswordRequest, VerifyPasswordResetOTP, ResetPasswordRequest
from auth.models import User
from auth.utils import hash_password, verify_password, create_access_token, create_password_reset_token, verify_password_reset_token, send_verification_email
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
    
    # Generate OTP and store it for verification
    otp = SUPER_OTP
    pending_verifications[request.email] = {"otp": otp, "type": "password_reset"}
    
    # Send OTP to user's email
    send_verification_email(request.email, otp)
    return {"msg": "Password reset OTP sent to your email."}

@router.post("/verify-password-reset-otp")
def verify_password_reset_otp(request: VerifyPasswordResetOTP):
    if request.email not in pending_verifications:
        raise HTTPException(status_code=400, detail="No pending password reset for this email.")
    
    pending_data = pending_verifications[request.email]
    if pending_data.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="No pending password reset for this email.")
    
    if request.otp != pending_data["otp"]:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    
    # Generate password reset token
    reset_token = create_password_reset_token(request.email)
    
    # Clean up pending verification
    pending_verifications.pop(request.email)
    
    return {"msg": "OTP verified. Use the reset token to change your password.", "reset_token": reset_token}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    # Verify the reset token
    email = verify_password_reset_token(request.reset_token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")
    
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Reset password
    users_db[email].hashed_password = hash_password(request.new_password)
    
    return {"msg": "Password reset successful."} 