"""JWT service for token management"""
from typing import Optional, Dict, Any
from app.core.security import SecurityUtils
from app.core.config import settings

class JWTService:
    """JWT service for creating and validating tokens"""

    @staticmethod
    def create_access_token(data: Dict[str, Any]) -> str:
        """Create access token"""
        return SecurityUtils.create_access_token(data)

    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create refresh token"""
        return SecurityUtils.create_refresh_token(data)
    
    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
        """Decode access token"""
        return SecurityUtils.decode_token(token, settings.JWT_SECRET_KEY)
    
    @staticmethod
    def decode_refresh_token(token: str) -> Optional[Dict[str, Any]]:
        """Decode refresh token"""
        return SecurityUtils.decode_token(token, settings.JWT_REFRESH_SECRET)
    
    @staticmethod
    def is_token_valid(token_data: Optional[Dict[str, Any]]) -> bool:
        """Check if token data is valid"""
        if not token_data:
            return False
        return SecurityUtils.verify_token_expiry(token_data)
