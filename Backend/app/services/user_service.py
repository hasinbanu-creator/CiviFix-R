"""User management service"""
from typing import List, Optional, Dict, Any
from app.db.mongodb import db
from app.repositories.user_repository import UserRepository
from app.core.exceptions import UserNotFoundException, DistrictAccessException
from datetime import datetime

class UserService:
    """Service for user management"""

    @staticmethod
    async def get_user_profile(user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        user = await UserRepository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        
        return {
            "id": str(user["_id"]),
            "name": user.get("name"),
            "email": user.get("email"),
            "mobile_number": user.get("mobile_number"),
            "address": user.get("address"),
            "district": user.get("district"),
            "role": user.get("role"),
            "status": user.get("status"),
            "is_verified": user.get("is_verified"),
            "is_active": user.get("is_active"),
            "created_at": user.get("created_at"),
            "last_login": user.get("last_login")
        }
    
    @staticmethod
    async def update_user_profile(
        user_id: str,
        name: Optional[str] = None,
        address: Optional[str] = None
    ) -> bool:
        """Update user profile"""
        
        update_data = {"updated_at": datetime.utcnow()}
        
        if name:
            update_data["name"] = name
        if address:
            update_data["address"] = address
        
        return await UserRepository.update_user(user_id, update_data)
    
    @staticmethod
    async def get_district_users(
        district: str,
        requesting_user_district: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get users from a district (with access control)"""
        
        # District isolation check
        if district != requesting_user_district:
            raise DistrictAccessException("Cannot access users from another district")
        
        users = await UserRepository.get_users_by_district(district, skip, limit)
        
        return [
            {
                "id": str(user["_id"]),
                "name": user.get("name"),
                "email": user.get("email"),
                "mobile_number": user.get("mobile_number"),
                "district": user.get("district"),
                "role": user.get("role"),
                "status": user.get("status"),
                "is_active": user.get("is_active"),
                "created_at": user.get("created_at")
            }
            for user in users
        ]
    
    @staticmethod
    async def get_users_by_role(
        role: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get users with specific role"""
        
        users = await UserRepository.get_users_by_role(role, skip, limit)
        
        return [
            {
                "id": str(user["_id"]),
                "name": user.get("name"),
                "email": user.get("email"),
                "district": user.get("district"),
                "role": user.get("role"),
                "status": user.get("status"),
                "created_at": user.get("created_at")
            }
            for user in users
        ]
    
    @staticmethod
    async def assign_role(user_id: str, role: str) -> bool:
        """Assign role to user"""
        return await UserRepository.update_user(
            user_id,
            {"role": role, "updated_at": datetime.utcnow()}
        )
    
    @staticmethod
    async def suspend_user(user_id: str) -> bool:
        """Suspend user account"""
        return await UserRepository.update_user(
            user_id,
            {
                "status": "SUSPENDED",
                "is_active": False,
                "updated_at": datetime.utcnow()
            }
        )
    
    @staticmethod
    async def activate_user(user_id: str) -> bool:
        """Activate user account"""
        return await UserRepository.update_user(
            user_id,
            {
                "status": "ACTIVE",
                "is_active": True,
                "updated_at": datetime.utcnow()
            }
        )
