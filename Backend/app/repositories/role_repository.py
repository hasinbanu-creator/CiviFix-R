"""Role repository for database operations"""
from typing import Optional, List
from bson import ObjectId
from app.db.mongodb import db
from app.core.exceptions import RoleNotFoundException

class RoleRepository:
    """Role data access layer"""
    
    roles_collection = db.roles
    permissions_collection = db.permissions
    
    @classmethod
    async def create_role(cls, role_data: dict) -> str:
        """Create a new role"""
        result = await cls.roles_collection.insert_one(role_data)
        return str(result.inserted_id)
    
    @classmethod
    async def find_role_by_id(cls, role_id: str) -> Optional[dict]:
        """Find role by ID"""
        try:
            return await cls.roles_collection.find_one({"_id": ObjectId(role_id)})
        except Exception:
            return None
    
    @classmethod
    async def find_role_by_name(cls, name: str) -> Optional[dict]:
        """Find role by name"""
        return await cls.roles_collection.find_one({"name": name})
    
    @classmethod
    async def get_all_roles(cls) -> List[dict]:
        """Get all roles"""
        cursor = cls.roles_collection.find({})
        return await cursor.to_list(length=None)
    
    @classmethod
    async def get_district_roles(cls, district: str) -> List[dict]:
        """Get roles for a specific district"""
        cursor = cls.roles_collection.find({"district": district})
        return await cursor.to_list(length=None)
    
    @classmethod
    async def update_role(cls, role_id: str, update_data: dict) -> bool:
        """Update role"""
        result = await cls.roles_collection.update_one(
            {"_id": ObjectId(role_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @classmethod
    async def add_permission_to_role(cls, role_id: str, permission_id: str) -> bool:
        """Add permission to role"""
        result = await cls.roles_collection.update_one(
            {"_id": ObjectId(role_id)},
            {"$addToSet": {"permissions": permission_id}}
        )
        return result.modified_count > 0
    
    @classmethod
    async def remove_permission_from_role(cls, role_id: str, permission_id: str) -> bool:
        """Remove permission from role"""
        result = await cls.roles_collection.update_one(
            {"_id": ObjectId(role_id)},
            {"$pull": {"permissions": permission_id}}
        )
        return result.modified_count > 0
    
    @classmethod
    async def create_permission(cls, permission_data: dict) -> str:
        """Create a new permission"""
        result = await cls.permissions_collection.insert_one(permission_data)
        return str(result.inserted_id)
    
    @classmethod
    async def find_permission_by_name(cls, name: str) -> Optional[dict]:
        """Find permission by name"""
        return await cls.permissions_collection.find_one({"name": name})
    
    @classmethod
    async def get_all_permissions(cls) -> List[dict]:
        """Get all permissions"""
        cursor = cls.permissions_collection.find({})
        return await cursor.to_list(length=None)
    
    @classmethod
    async def get_role_permissions(cls, role_id: str) -> List[dict]:
        """Get all permissions for a role"""
        role = await cls.find_role_by_id(role_id)
        if not role:
            return []
        
        permission_ids = role.get("permissions", [])
        cursor = cls.permissions_collection.find(
            {"_id": {"$in": [ObjectId(pid) if isinstance(pid, str) else pid for pid in permission_ids]}}
        )
        return await cursor.to_list(length=None)
