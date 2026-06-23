"""Token-related schemas"""
from pydantic import BaseModel, Field
from typing import Optional

class TokenDataSchema(BaseModel):
    """Token data schema"""
    user_id: str
    email: str
    role: str
    district: str
    permissions: list = []

    class Config:
        example = {
            "user_id": "507f1f77bcf86cd799439011",
            "email": "user@gmail.com",
            "role": "CITIZEN",
            "district": "Chennai",
            "permissions": ["view_own_profile"]
        }


class AccessTokenSchema(BaseModel):
    """Access token schema"""
    token: str = Field(..., description="JWT access token")
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token expiry in seconds")


class RefreshTokenDataSchema(BaseModel):
    """Refresh token data"""
    user_id: str
    type: str = "refresh"
