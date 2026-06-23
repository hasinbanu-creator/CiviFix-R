"""OTP service for generation and verification"""
from datetime import datetime, timedelta
from app.utils.otp_generator import generate_otp
from app.core.security import SecurityUtils
from app.core.config import settings

class OTPService:
    """OTP service for handling OTP generation and hashing"""

    @staticmethod
    async def create_otp() -> tuple:
        """Create OTP with hash and expiry"""
        otp = generate_otp()
        otp_hash = SecurityUtils.hash_otp(otp)
        expiry = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        
        return otp, otp_hash, expiry
    
    @staticmethod
    def verify_otp(otp: str, otp_hash: str) -> bool:
        """Verify OTP against hash"""
        return SecurityUtils.verify_otp(otp, otp_hash)
