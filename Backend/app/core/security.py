from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class SecurityUtils:
    """Centralized security utilities for password and token handling"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_otp(otp: str) -> str:
        """Hash OTP for secure storage"""
        return pwd_context.hash(otp)

    @staticmethod
    def verify_otp(plain_otp: str, hashed_otp: str) -> bool:
        """Verify OTP against hash"""
        return pwd_context.verify(plain_otp, hashed_otp)

    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_REFRESH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(
        token: str,
        secret_key: str = settings.JWT_SECRET_KEY
    ) -> Optional[Dict[str, Any]]:
        """Decode JWT token safely"""
        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def verify_token_expiry(token_data: Dict[str, Any]) -> bool:
        """Check if token is expired"""
        if "exp" not in token_data:
            return False
        
        exp_timestamp = token_data["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        
        return exp_timestamp > current_timestamp
