"""Role and permission management service"""
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.db.mongodb import db
from app.repositories.role_repository import RoleRepository
from app.core.exceptions import RoleNotFoundException
from app.models.role_model import role_document, permission_document, DEFAULT_PERMISSIONS
from datetime import datetime

class RoleService:
    """Service for role and permission management"""

    @staticmethod
    async def create_default_roles(district: Optional[str] = None) -> None:
        """Create default system roles"""
        
        roles_to_create = [
            ("SUPER_ADMIN", "Super administrator with full access", True, None),
            ("DISTRICT_ADMIN", "District administrator", True, district),
            ("INSPECTOR", "Complaint inspector", True, district),
            ("WORKER", "Field worker", True, district),
            ("CITIZEN", "Regular citizen", True, None),
        ]
        
        for role_name, description, is_system, dist in roles_to_create:
            existing = await RoleRepository.find_role_by_name(role_name)
            if not existing:
                permissions = DEFAULT_PERMISSIONS.get(role_name, [])
                role_data = role_document(
                    name=role_name,
                    description=description,
                    permissions=permissions,
                    is_system=is_system,
                    district=dist
                )
                await RoleRepository.create_role(role_data)
    
    @staticmethod
    async def create_custom_role(
        name: str,
        description: str,
        permissions: List[str],
        district: str
    ) -> str:
        """Create custom role for a district"""
        
        # Check if role already exists
        existing = await RoleRepository.find_role_by_name(name)
        if existing:
            raise ValueError(f"Role {name} already exists")
        
        role_data = role_document(
            name=name,
            description=description,
            permissions=permissions,
            is_system=False,
            district=district
        )
        
        return await RoleRepository.create_role(role_data)
    
    @staticmethod
    async def get_role_permissions(role_id: str) -> List[Dict[str, Any]]:
        """Get all permissions for a role"""
        
        role = await RoleRepository.find_role_by_id(role_id)
        if not role:
            raise RoleNotFoundException("Role not found")
        
        return await RoleRepository.get_role_permissions(role_id)
    
    @staticmethod
    async def check_permission(user_role: str, required_permission: str) -> bool:
        """Check if user role has required permission"""
        
        role = await RoleRepository.find_role_by_name(user_role)
        if not role:
            return False
        
        return required_permission in role.get("permissions", [])
    
    @staticmethod
    async def create_permission(
        name: str,
        description: str = "",
        category: str = "general"
    ) -> str:
        """Create a new permission"""
        
        permission_data = permission_document(
            name=name,
            description=description,
            category=category
        )
        
        return await RoleRepository.create_permission(permission_data)
    
    @staticmethod
    async def add_permission_to_role(role_id: str, permission_id: str) -> bool:
        """Add permission to role"""
        return await RoleRepository.add_permission_to_role(role_id, permission_id)
    
    @staticmethod
    async def remove_permission_from_role(role_id: str, permission_id: str) -> bool:
        """Remove permission from role"""
        return await RoleRepository.remove_permission_from_role(role_id, permission_id)
