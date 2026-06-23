"""District management service"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.repositories.district_repository import DistrictRepository
from app.models.district_model import district_document


class DistrictService:
    """Service for district management"""
    
    @staticmethod
    async def create_district(
        name: str,
        code: str,
        state: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        created_by_id: Optional[str] = None
    ) -> str:
        """Create a new district"""
        
        # Check if code already exists
        existing = await DistrictRepository.find_by_code(code)
        if existing:
            raise ValueError(f"District code '{code}' already exists")
        
        # Check if name already exists
        existing_name = await DistrictRepository.find_by_name(name)
        if existing_name:
            raise ValueError(f"District name '{name}' already exists")
        
        # Create district document
        class DistrictData:
            pass
        
        data = DistrictData()
        data.name = name
        data.code = code
        data.state = state
        data.email = email
        data.phone = phone
        data.address = address
        data.created_by = created_by_id
        
        district_data = district_document(data)
        
        # Insert into database
        district_id = await DistrictRepository.create_district(district_data)
        return district_id
    
    @staticmethod
    async def get_district(district_id: str) -> Optional[Dict[str, Any]]:
        """Get district by ID"""
        return await DistrictRepository.find_by_id(district_id)
    
    @staticmethod
    async def get_all_districts() -> List[Dict[str, Any]]:
        """Get all districts"""
        return await DistrictRepository.get_all_districts()
    
    @staticmethod
    async def get_active_districts() -> List[Dict[str, Any]]:
        """Get all active districts"""
        return await DistrictRepository.get_active_districts()
    
    @staticmethod
    async def update_district(
        district_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None
    ) -> bool:
        """Update district information"""
        
        update_data = {}
        if name is not None:
            # Check if new name already exists
            existing = await DistrictRepository.find_by_name(name)
            if existing and existing.get("_id") != ObjectId(district_id):
                raise ValueError(f"District name '{name}' already exists")
            update_data["name"] = name
        
        if email is not None:
            update_data["email"] = email
        if phone is not None:
            update_data["phone"] = phone
        if address is not None:
            update_data["address"] = address
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            return await DistrictRepository.update_district(district_id, update_data)
        
        return False
    
    @staticmethod
    async def activate_district(district_id: str) -> bool:
        """Activate a district"""
        return await DistrictRepository.activate_district(district_id)
    
    @staticmethod
    async def deactivate_district(district_id: str) -> bool:
        """Deactivate a district"""
        return await DistrictRepository.deactivate_district(district_id)
    
    @staticmethod
    async def delete_district(district_id: str) -> bool:
        """Delete a district"""
        return await DistrictRepository.delete_district(district_id)
