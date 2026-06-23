"""District schemas for API validation"""
from pydantic import BaseModel, Field
from typing import Optional


class CreateDistrictSchema(BaseModel):
    """Schema for creating a new district"""
    name: str = Field(..., min_length=2, max_length=100, description="District name")
    code: str = Field(..., min_length=2, max_length=10, description="District code (unique)")
    state: str = Field(default="Tamil Nadu", max_length=50, description="State name")
    email: Optional[str] = Field(None, description="District email")
    phone: Optional[str] = Field(None, description="District phone")
    address: Optional[str] = Field(None, description="District address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Chennai",
                "code": "CHN",
                "state": "Tamil Nadu",
                "email": "admin@chennai.tn.in",
                "phone": "9876543210",
                "address": "Chennai District Headquarters"
            }
        }


class UpdateDistrictSchema(BaseModel):
    """Schema for updating a district"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "newemail@chennai.tn.in",
                "phone": "9988776655"
            }
        }


class DistrictResponseSchema(BaseModel):
    """Schema for district response"""
    id: str = Field(..., alias="_id", description="District ID")
    name: str = Field(..., description="District name")
    code: str = Field(..., description="District code")
    state: str = Field(..., description="State name")
    email: Optional[str] = Field(None, description="District email")
    phone: Optional[str] = Field(None, description="District phone")
    address: Optional[str] = Field(None, description="District address")
    is_active: bool = Field(default=True, description="Active status")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Update timestamp")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "Chennai",
                "code": "CHN",
                "state": "Tamil Nadu",
                "email": "admin@chennai.tn.in",
                "phone": "9876543210",
                "address": "Chennai District Headquarters",
                "is_active": True,
                "created_at": "2026-05-26T00:00:00",
                "updated_at": "2026-05-26T00:00:00"
            }
        }
