from typing import Dict
from auth.models import User

users_db: Dict[str, User] = {}
pending_verifications: Dict[str, str] = {}  # email -> otp 