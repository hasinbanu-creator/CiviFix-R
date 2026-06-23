"""User model for MongoDB"""
from datetime import datetime
from typing import Optional, List

def user_document(data) -> dict:
    """Create a user document for MongoDB"""
    return {
        "name": data.name,
        "address": data.address,
        "mobile_number": data.mobile_number,
        "email": data.email,
        "district": data.district,
        
        "role": data.role if hasattr(data, "role") else "CITIZEN",
        "permissions": [],
        
        # OTP fields
        "otp_code_hash": None,
        "otp_expiry": None,
        "otp_attempts": 0,
        "otp_last_request_at": None,
        "otp_resend_count": 0,
        
        # Account status
        "is_verified": False,
        "is_active": False,
        "status": "INACTIVE",
        
        # Account metadata
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None,
        
        # Optional fields
        "phone_verified_at": None,
        "email_verified_at": None
    }


def admin_user_document(data) -> dict:
    """Create an admin user document"""
    doc = user_document(data)
    doc["role"] = data.role if hasattr(data, "role") else "DISTRICT_ADMIN"
    doc["is_verified"] = True
    doc["is_active"] = True
    doc["status"] = "ACTIVE"
    doc["created_by"] = data.created_by if hasattr(data, "created_by") else None
    return doc
