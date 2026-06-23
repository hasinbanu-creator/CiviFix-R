from enum import Enum


class Roles(str, Enum):
    """User role definitions"""
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    DISTRICT_ADMIN = "DISTRICT_ADMIN"
    INSPECTOR = "INSPECTOR"
    WORKER = "WORKER"
    CITIZEN = "CITIZEN"


class ComplaintStatus(str, Enum):
    """Complaint lifecycle statuses"""
    OPEN = "OPEN"
    WORKING = "WORKING"
    APPROVAL = "APPROVAL"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"


class ComplaintType(str, Enum):
    """Types of complaints"""
    GARBAGE = "GARBAGE"
    ROAD_DAMAGE = "ROAD_DAMAGE"
    POTHOLE = "POTHOLE"
    STREETLIGHT = "STREETLIGHT"
    WATER_SUPPLY = "WATER_SUPPLY"
    DRAINAGE = "DRAINAGE"
    SANITATION = "SANITATION"
    TREE_CUTTING = "TREE_CUTTING"
    CONSTRUCTION = "CONSTRUCTION"
    OTHER = "OTHER"


class Priority(str, Enum):
    """Complaint priority levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ComplaintHistoryAction(str, Enum):
    """Actions tracked in complaint history"""
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    STATUS_CHANGED = "STATUS_CHANGED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"
    IMAGE_ADDED = "IMAGE_ADDED"
    NOTE_ADDED = "NOTE_ADDED"


class NotificationType(str, Enum):
    """Types of notifications"""
    EMAIL = "EMAIL"
    PUSH = "PUSH"
    IN_APP = "IN_APP"


class NotificationStatus(str, Enum):
    """Notification delivery status"""
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    DELIVERED = "DELIVERED"