"""OTP-related schemas"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class SendOTPSchema(BaseModel):
    """Send OTP schema"""
    email: EmailStr
    
    class Config:
        example = {
            "email": "user@gmail.com"
        }


class OTPResponseSchema(BaseModel):
    """OTP response schema"""
    email: str
    otp_sent: bool
    expires_in: int  # seconds
    message: str

    class Config:
        example = {
            "email": "user@gmail.com",
            "otp_sent": True,
            "expires_in": 300,
            "message": "OTP sent to email"
        }
