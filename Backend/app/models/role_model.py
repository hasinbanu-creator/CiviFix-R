"""Role and Permission models for MongoDB"""
from datetime import datetime
from typing import List, Optional

def role_document(
    name: str,
    description: str = "",
    permissions: List[str] = None,
    is_system: bool = False,
    district: Optional[str] = None
) -> dict:
    """Create a role document"""
    return {
        "name": name,
        "description": description,
        "permissions": permissions or [],
        "is_system": is_system,
        "district": district,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


def permission_document(
    name: str,
    description: str = "",
    category: str = "general"
) -> dict:
    """Create a permission document"""
    return {
        "name": name,
        "description": description,
        "category": category,
        "created_at": datetime.utcnow()
    }


def role_permission_mapping(
    role_id: str,
    permission_ids: List[str]
) -> dict:
    """Create role-permission mapping"""
    return {
        "role_id": role_id,
        "permission_ids": permission_ids,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


# Default permissions for each role
DEFAULT_PERMISSIONS = {
    "CITIZEN": [
        "view_own_profile",
        "view_own_complaints",
        "create_complaint",
        "update_own_profile"
    ],
    "WORKER": [
        "view_assigned_complaints",
        "update_complaint_status",
        "view_own_profile",
        "update_own_profile"
    ],
    "INSPECTOR": [
        "view_assigned_complaints",
        "approve_complaint",
        "reject_complaint",
        "assign_complaint",
        "view_complaint_history",
        "view_own_profile",
        "update_own_profile"
    ],
    "DISTRICT_ADMIN": [
        "create_inspector",
        "create_worker",
        "create_custom_roles",
        "view_district_users",
        "assign_roles",
        "view_all_complaints",
        "manage_district_users",
        "view_own_profile",
        "update_own_profile"
    ],
    "SUPER_ADMIN": [
        "manage_all_users",
        "manage_all_roles",
        "manage_all_permissions",
        "view_all_data",
        "system_configuration",
        "view_logs",
        "manage_districts"
    ]
}
