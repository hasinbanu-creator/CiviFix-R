"""District model for MongoDB"""
from datetime import datetime
from typing import Optional


def district_document(data) -> dict:
    """Create a district document for MongoDB"""
    return {
        "name": data.name,
        "code": data.code,
        "state": data.state if hasattr(data, "state") else "Tamil Nadu",
        "admin_id": data.admin_id if hasattr(data, "admin_id") else None,
        "email": data.email if hasattr(data, "email") else None,
        "phone": data.phone if hasattr(data, "phone") else None,
        "address": data.address if hasattr(data, "address") else None,
        "is_active": True,
        "created_by": data.created_by if hasattr(data, "created_by") else None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
