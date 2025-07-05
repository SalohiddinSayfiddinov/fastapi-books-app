from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from auth.schemas import UserCreate, UserLogin, UserVerify, ForgotPasswordRequest, VerifyPasswordResetOTP, ResetPasswordRequest, UserResponse, TokenResponse
from auth.models import User
from auth.utils import hash_password, verify_password, create_access_token, create_password_reset_token, verify_password_reset_token, send_verification_email
from database import get_db
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

SUPER_OTP = "1234"

# In-memory storage for pending verifications (could be moved to database later)
pending_verifications = {}

@router.post("/signup", response_model=dict)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    # Check if email is pending verification
    if user.email in pending_verifications:
        raise HTTPException(status_code=400, detail="Email already pending verification.")
    
    otp = SUPER_OTP
    pending_verifications[user.email] = {
        "hashed_password": hash_password(user.password), 
        "name": user.name
    }
    send_verification_email(user.email, otp)
    return {"msg": "Verification code sent to your email."}

@router.post("/verify", response_model=dict)
def verify(data: UserVerify, db: Session = Depends(get_db)):
    if data.email not in pending_verifications:
        raise HTTPException(status_code=400, detail="No pending verification for this email.")
    
    if data.otp != SUPER_OTP:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    
    pending = pending_verifications.pop(data.email)
    
    # Create new user in database
    db_user = User(
        email=data.email,
        name=pending["name"],
        hashed_password=pending["hashed_password"],
        is_verified=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"msg": "Email verified. You can now log in."}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not db_user.is_verified or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials or email not verified.")
    
    access_token = create_access_token({"sub": db_user.email})
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/forgot-password", response_model=dict)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Generate OTP and store it for verification
    otp = SUPER_OTP
    pending_verifications[request.email] = {"otp": otp, "type": "password_reset"}
    
    # Send OTP to user's email
    send_verification_email(request.email, otp)
    return {"msg": "Password reset OTP sent to your email."}

@router.post("/verify-password-reset-otp", response_model=dict)
def verify_password_reset_otp(request: VerifyPasswordResetOTP, db: Session = Depends(get_db)):
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

@router.post("/reset-password", response_model=dict)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Verify the reset token
    email = verify_password_reset_token(request.reset_token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")
    
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Reset password
    db_user.hashed_password = hash_password(request.new_password)
    db.commit()
    
    return {"msg": "Password reset successful."} 