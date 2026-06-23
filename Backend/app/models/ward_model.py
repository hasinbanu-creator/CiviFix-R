"""Ward/Zone model for MongoDB"""
from datetime import datetime


def ward_document(data) -> dict:
    """Create a ward document for MongoDB"""
    return {
        "district_id": data.district_id,
        "ward_name": data.ward_name,
        "ward_number": data.ward_number,
        "inspector_id": data.inspector_id if hasattr(data, "inspector_id") else None,
        "description": data.description if hasattr(data, "description") else None,
        "area_coordinates": data.area_coordinates if hasattr(data, "area_coordinates") else None,
        "is_active": True,
        "complaint_count": 0,
        "active_complaints": 0,
        "closed_complaints": 0,
        "created_by": data.created_by if hasattr(data, "created_by") else None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
