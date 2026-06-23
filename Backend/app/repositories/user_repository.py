"""User repository for database operations"""
from typing import Optional, List
from bson import ObjectId
from app.db.mongodb import db
from app.core.exceptions import UserNotFoundException, UserAlreadyExistsException

class UserRepository:
    """User data access layer"""
    
    collection = db.users
    
    @classmethod
    async def create_user(cls, user_data: dict) -> str:
        """Create a new user and return user ID"""
        existing = await cls.collection.find_one({
            "$or": [
                {"email": user_data.get("email")},
                {"mobile_number": user_data.get("mobile_number")}
            ]
        })
        
        if existing:
            raise UserAlreadyExistsException()
        
        result = await cls.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @classmethod
    async def find_by_id(cls, user_id: str) -> Optional[dict]:
        """Find user by ID"""
        try:
            return await cls.collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    @classmethod
    async def get_by_id(cls, user_id: str) -> Optional[dict]:
        """Alias for find_by_id to support services expecting get_by_id"""
        return await cls.find_by_id(user_id)
    
    @classmethod
    async def find_by_email(cls, email: str) -> Optional[dict]:
        """Find user by email"""
        return await cls.collection.find_one({"email": email})
    
    @classmethod
    async def find_by_mobile(cls, mobile_number: str) -> Optional[dict]:
        """Find user by mobile number"""
        return await cls.collection.find_one({"mobile_number": mobile_number})
    
    @classmethod
    async def update_user(cls, user_id: str, update_data: dict) -> bool:
        """Update user data"""
        try:
            result = await cls.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    @classmethod
    async def verify_user(cls, user_id: str) -> bool:
        """Mark user as verified and activate account"""
        return await cls.update_user(
            user_id,
            {
                "is_verified": True,
                "is_active": True,
                "status": "ACTIVE",
                "email_verified_at": __import__('datetime').datetime.utcnow()
            }
        )
    
    @classmethod
    async def update_otp(
        cls,
        email: str,
        otp_hash: str,
        expiry: __import__('datetime').datetime
    ) -> bool:
        """Update OTP for user"""
        return await cls.update_user(
            None,
            {
                "otp_code_hash": otp_hash,
                "otp_expiry": expiry,
                "otp_attempts": 0,
                "otp_last_request_at": __import__('datetime').datetime.utcnow()
            }
        ) if await cls.find_by_email(email) else False
    
    @classmethod
    async def get_users_by_district(
        cls,
        district: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[dict]:
        """Get users by district with pagination"""
        cursor = cls.collection.find({"district": district}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    @classmethod
    async def get_users_by_role(
        cls,
        role: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[dict]:
        """Get users by role with pagination"""
        cursor = cls.collection.find({"role": role}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    @classmethod
    async def delete_user(cls, user_id: str) -> bool:
        """Delete user (soft delete via status)"""
        return await cls.update_user(
            user_id,
            {"status": "INACTIVE", "is_active": False}
        )
    
    @classmethod
    async def count_users(cls, query: dict = None) -> int:
        """Count total users"""
        return await cls.collection.count_documents(query or {})
