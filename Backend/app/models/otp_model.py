"""OTP Log model for MongoDB"""
from datetime import datetime
from typing import Optional

def otp_log_document(
    identifier: str,
    identifier_type: str,  # "email" or "mobile"
    otp_hash: str,
    expires_at: datetime,
    purpose: str = "registration"  # registration, login, password_reset
) -> dict:
    """Create an OTP log document for audit and tracking"""
    return {
        "identifier": identifier,
        "identifier_type": identifier_type,
        "otp_hash": otp_hash,
        "expires_at": expires_at,
        "purpose": purpose,
        "attempts": 0,
        "max_attempts": 5,
        "is_verified": False,
        "verified_at": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
