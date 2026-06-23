"""Token and Refresh Token models for MongoDB"""
from datetime import datetime
from typing import Optional

def refresh_token_document(
    user_id: str,
    token_hash: str,
    expires_at: datetime,
    device_id: Optional[str] = None,
    ip_address: Optional[str] = None
) -> dict:
    """Create a refresh token document for secure storage and rotation"""
    return {
        "user_id": user_id,
        "token_hash": token_hash,
        "expires_at": expires_at,
        "is_revoked": False,
        "revoked_at": None,
        "device_id": device_id,
        "ip_address": ip_address,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_used_at": datetime.utcnow()
    }


def token_blacklist_document(
    user_id: str,
    token_hash: str,
    token_type: str,  # "access" or "refresh"
    expires_at: datetime,
    reason: str = "logout"
) -> dict:
    """Create a token blacklist document"""
    return {
        "user_id": user_id,
        "token_hash": token_hash,
        "token_type": token_type,
        "expires_at": expires_at,
        "reason": reason,
        "created_at": datetime.utcnow()
    }
