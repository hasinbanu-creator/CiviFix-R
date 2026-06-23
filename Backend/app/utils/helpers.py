"""Helper functions"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import secrets
import string
from bson import ObjectId


def generate_random_string(length: int = 32) -> str:
    """Generate random string for tokens"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def get_remaining_time(expiry: datetime) -> Optional[int]:
    """Get remaining time in seconds"""
    if not expiry:
        return None
    
    now = datetime.utcnow()
    if expiry <= now:
        return 0
    
    return int((expiry - now).total_seconds())


def is_expired(expiry: datetime) -> bool:
    """Check if datetime is expired"""
    return datetime.utcnow() > expiry


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    if not dt:
        return None
    return dt.strftime(format_str)


def dict_to_object(dict_data: dict, **kwargs) -> object:
    """Convert dict to object"""
    class DictObject:
        def __init__(self, **entries):
            self.__dict__.update(entries)
    
    return DictObject(**{**dict_data, **kwargs})


def sanitize_phone(phone: str) -> str:
    """Sanitize phone number"""
    return ''.join(filter(str.isdigit, phone))


def serialize_mongo_document(document: dict) -> dict:
    """Convert MongoDB document fields to JSON-safe values."""
    if not isinstance(document, dict):
        return document

    serialized: dict = {}
    for key, value in document.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, dict):
            serialized[key] = serialize_mongo_document(value)
        elif isinstance(value, list):
            serialized[key] = [serialize_mongo_document(item) if isinstance(item, dict) else str(item) if isinstance(item, ObjectId) else item for item in value]
        else:
            serialized[key] = value
    return serialized


def serialize_mongo_documents(documents: List[dict]) -> List[dict]:
    """Serialize a list of MongoDB documents."""
    return [serialize_mongo_document(doc) for doc in documents]


def extract_user_agent(user_agent_str: str) -> Dict[str, Any]:
    """Extract browser/device info from user agent"""
    return {
        "user_agent": user_agent_str,
        "is_mobile": "mobile" in user_agent_str.lower(),
    }
