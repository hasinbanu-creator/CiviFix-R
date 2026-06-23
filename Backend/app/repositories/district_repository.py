"""District repository for database operations"""
from typing import Optional, List
from bson import ObjectId
from app.db.mongodb import db


class DistrictRepository:
    """District data access layer"""
    
    collection = db.districts
    
    @classmethod
    async def create_district(cls, district_data: dict) -> str:
        """Create a new district"""
        result = await cls.collection.insert_one(district_data)
        return str(result.inserted_id)
    
    @classmethod
    async def find_by_id(cls, district_id: str) -> Optional[dict]:
        """Find district by ID"""
        try:
            return await cls.collection.find_one({"_id": ObjectId(district_id)})
        except Exception:
            return None
    
    @classmethod
    async def find_by_code(cls, code: str) -> Optional[dict]:
        """Find district by code"""
        return await cls.collection.find_one({"code": code})
    
    @classmethod
    async def find_by_name(cls, name: str) -> Optional[dict]:
        """Find district by name"""
        return await cls.collection.find_one({"name": name})
    
    @classmethod
    async def get_all_districts(cls) -> List[dict]:
        """Get all districts"""
        cursor = cls.collection.find({})
        return await cursor.to_list(length=None)
    
    @classmethod
    async def get_active_districts(cls) -> List[dict]:
        """Get all active districts"""
        cursor = cls.collection.find({"is_active": True})
        return await cursor.to_list(length=None)
    
    @classmethod
    async def update_district(cls, district_id: str, update_data: dict) -> bool:
        """Update district"""
        result = await cls.collection.update_one(
            {"_id": ObjectId(district_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @classmethod
    async def activate_district(cls, district_id: str) -> bool:
        """Activate a district"""
        return await cls.update_district(district_id, {"is_active": True})
    
    @classmethod
    async def deactivate_district(cls, district_id: str) -> bool:
        """Deactivate a district"""
        return await cls.update_district(district_id, {"is_active": False})
    
    @classmethod
    async def delete_district(cls, district_id: str) -> bool:
        """Delete a district"""
        result = await cls.collection.delete_one({"_id": ObjectId(district_id)})
        return result.deleted_count > 0
    
    @classmethod
    async def check_code_exists(cls, code: str, exclude_id: Optional[str] = None) -> bool:
        """Check if district code already exists"""
        query = {"code": code}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        return await cls.collection.find_one(query) is not None
