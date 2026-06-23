"""Notification model for MongoDB"""
from datetime import datetime
from typing import Optional


def notification_document(data) -> dict:
    """Create a notification document for MongoDB"""
    return {
        "user_id": data.user_id,
        "complaint_id": data.complaint_id if hasattr(data, "complaint_id") else None,
        "type": data.type,
        "channel": data.channel,  # EMAIL, PUSH, IN_APP
        "title": data.title,
        "message": data.message,
        "status": "PENDING",  # PENDING, SENT, FAILED, DELIVERED
        "recipient": data.recipient,  # Email or phone
        "metadata": data.metadata if hasattr(data, "metadata") else {},
        "created_at": datetime.utcnow(),
        "sent_at": None,
        "delivered_at": None,
        "retry_count": 0,
        "last_error": None,
    }
