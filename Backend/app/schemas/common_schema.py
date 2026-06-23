"""Common schemas used across the application"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")


class ErrorSchema(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str
    error_code: str
    errors: Optional[dict] = None


class SuccessSchema(BaseModel):
    """Generic success response schema"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class PaginationSchema(BaseModel):
    """Pagination schema"""
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    skip: int = Field(0, ge=0)
    
    @property
    def get_skip(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponseSchema(BaseModel, Generic[T]):
    """Paginated response schema"""
    success: bool = True
    message: str
    data: list[T]
    pagination: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True


class OTPSchema(BaseModel):
    """OTP schema"""
    email: str
    otp_expiry: datetime
    attempts_remaining: int
    resend_available_in: Optional[int] = None


class RoleSchema(BaseModel):
    """Role schema"""
    id: str = Field(..., alias="_id")
    name: str
    description: str
    permissions: list
    is_system: bool
    created_at: datetime

    class Config:
        populate_by_name = True


class PermissionSchema(BaseModel):
    """Permission schema"""
    id: str = Field(..., alias="_id")
    name: str
    description: str
    category: str
    created_at: datetime

    class Config:
        populate_by_name = True


class HealthCheckSchema(BaseModel):
    """Health check response"""
    status: str = "healthy"
    service: str = "Civifix API"
    version: str = "1.0.0"
    timestamp: datetime
