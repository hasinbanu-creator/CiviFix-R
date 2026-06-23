"""District isolation dependencies"""
from fastapi import Depends, HTTPException, status
from typing import Dict, Any
from app.dependencies.auth_dependency import get_current_user


async def check_district_access(
    target_district: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Check if user has access to target district"""
    
    user_role = current_user.get("role")
    user_district = current_user.get("district")
    
    # Super admin can access all districts
    if user_role == "SUPER_ADMIN":
        return current_user
    
    # Other roles can only access their own district
    if user_district != target_district:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access resources from another district"
        )
    
    return current_user


def require_same_district(*district_fields: str):
    """Verify that user is from the same district as the resource"""
    async def district_checker(
        current_user: Dict[str, Any] = Depends(get_current_user),
        target_district: str = None
    ) -> Dict[str, Any]:
        
        user_role = current_user.get("role")
        user_district = current_user.get("district")
        
        if user_role == "SUPER_ADMIN":
            return current_user
        
        if user_district != target_district:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access resources from another district"
            )
        
        return current_user
    
    return district_checker
