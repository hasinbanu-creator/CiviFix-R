"""OTP repository for database operations"""
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.db.mongodb import db

class OTPRepository:
    """OTP data access layer"""
    
    collection = db.otp_logs
    
    @classmethod
    async def create_otp_log(cls, otp_data: dict) -> str:
        """Create OTP log entry"""
        result = await cls.collection.insert_one(otp_data)
        return str(result.inserted_id)
    
    @classmethod
    async def find_latest_otp(cls, identifier: str) -> Optional[dict]:
        """Find latest OTP for identifier (email/mobile)"""
        return await cls.collection.find_one(
            {"identifier": identifier},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def update_otp(cls, otp_id: str, update_data: dict) -> bool:
        """Update OTP log"""
        result = await cls.collection.update_one(
            {"_id": ObjectId(otp_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @classmethod
    async def increment_attempts(cls, identifier: str) -> bool:
        """Increment OTP attempts"""
        result = await cls.collection.update_one(
            {"identifier": identifier, "is_verified": False},
            {"$inc": {"attempts": 1}, "$set": {"updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    @classmethod
    async def mark_verified(cls, identifier: str) -> bool:
        """Mark OTP as verified"""
        result = await cls.collection.update_one(
            {"identifier": identifier, "is_verified": False},
            {
                "$set": {
                    "is_verified": True,
                    "verified_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @classmethod
    async def is_otp_valid(cls, identifier: str) -> bool:
        """Check if OTP is still valid"""
        otp = await cls.find_latest_otp(identifier)
        if not otp:
            return False
        
        if otp.get("is_verified"):
            return False
        
        if otp.get("attempts", 0) >= otp.get("max_attempts", 5):
            return False
        
        if datetime.utcnow() > otp.get("expires_at"):
            return False
        
        return True
    
    @classmethod
    async def get_otp_attempts_remaining(cls, identifier: str) -> int:
        """Get remaining OTP attempts"""
        otp = await cls.find_latest_otp(identifier)
        if not otp:
            return 0
        
        max_attempts = otp.get("max_attempts", 5)
        current_attempts = otp.get("attempts", 0)
        return max(0, max_attempts - current_attempts)
    
    @classmethod
    async def cleanup_expired_otps(cls, days: int = 7) -> int:
        """Delete OTP logs older than specified days"""
        cutoff_date = datetime.utcnow() - __import__('datetime').timedelta(days=days)
        result = await cls.collection.delete_many(
            {"created_at": {"$lt": cutoff_date}}
        )
        return result.deleted_count
