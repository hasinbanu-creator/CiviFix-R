"""Validation utilities"""
import re
from email_validator import validate_email as validate_email_lib
from email_validator import EmailNotValidError

def validate_mobile(mobile: str) -> bool:
    """Validate Indian mobile number format"""
    pattern = r"^[6-9]\d{9}$"
    return bool(re.match(pattern, mobile))


def validate_email(email: str) -> bool:
    """Validate email format"""
    try:
        validate_email_lib(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def validate_name(name: str) -> bool:
    """Validate name length and characters"""
    if not name or len(name) < 2 or len(name) > 100:
        return False
    return True


def validate_password_strength(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit


def validate_otp(otp: str) -> bool:
    """Validate OTP format"""
    pattern = r"^\d{6}$"
    return bool(re.match(pattern, otp))


def validate_district(district: str) -> bool:
    """Validate district name"""
    if not district or len(district) < 2 or len(district) > 50:
        return False
    return True


def validate_address(address: str) -> bool:
    """Validate address"""
    if not address or len(address) < 5 or len(address) > 200:
        return False
    return True
