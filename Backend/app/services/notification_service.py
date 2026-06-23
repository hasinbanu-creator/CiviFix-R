"""Notification service for email, push, and in-app notifications"""
from typing import Optional
from datetime import datetime
import logging

from app.core.enums import NotificationType, NotificationStatus

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for handling notifications"""

    def __init__(self, email_service=None, notification_repo=None):
        self.email_service = email_service
        self.notification_repo = notification_repo

    async def notify_complaint_created(
        self,
        complaint_id: str,
        inspector_id: str,
        complaint_number: str
    ) -> bool:
        """Notify inspector when complaint is created"""
        try:
            title = "New Complaint Assigned"
            message = f"New complaint {complaint_number} has been assigned to you"
            
            # Send email
            if self.email_service:
                await self.email_service.send_complaint_notification(
                    inspector_id,
                    title,
                    message
                )
            
            # Store notification record
            if self.notification_repo:
                await self.notification_repo.create({
                    "user_id": inspector_id,
                    "complaint_id": complaint_id,
                    "type": NotificationType.EMAIL,
                    "title": title,
                    "message": message,
                    "status": NotificationStatus.SENT,
                    "created_at": datetime.utcnow()
                })
            
            logger.info(f"Complaint creation notification sent to inspector {inspector_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending complaint notification: {str(e)}")
            return False

    async def notify_worker_assigned(
        self,
        complaint_id: str,
        worker_id: str,
        deadline: datetime
    ) -> bool:
        """Notify worker when assigned to complaint"""
        try:
            title = "New Task Assigned"
            message = f"You have been assigned a new task with deadline {deadline.strftime('%Y-%m-%d')}"
            
            if self.email_service:
                await self.email_service.send_task_notification(
                    worker_id,
                    title,
                    message,
                    deadline
                )
            
            if self.notification_repo:
                await self.notification_repo.create({
                    "user_id": worker_id,
                    "complaint_id": complaint_id,
                    "type": NotificationType.EMAIL,
                    "title": title,
                    "message": message,
                    "status": NotificationStatus.SENT,
                    "created_at": datetime.utcnow()
                })
            
            logger.info(f"Worker assignment notification sent to {worker_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending worker assignment: {str(e)}")
            return False

    async def notify_work_submitted(
        self,
        complaint_id: str,
        inspector_id: str
    ) -> bool:
        """Notify inspector when worker submits work"""
        try:
            title = "Work Submitted for Review"
            message = "A worker has submitted their work and is awaiting your approval"
            
            if self.email_service:
                await self.email_service.send_approval_notification(
                    inspector_id,
                    title,
                    message
                )
            
            if self.notification_repo:
                await self.notification_repo.create({
                    "user_id": inspector_id,
                    "complaint_id": complaint_id,
                    "type": NotificationType.EMAIL,
                    "title": title,
                    "message": message,
                    "status": NotificationStatus.SENT,
                    "created_at": datetime.utcnow()
                })
            
            logger.info(f"Work submission notification sent to inspector {inspector_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending submission notification: {str(e)}")
            return False

    async def notify_complaint_approved(
        self,
        complaint_id: str,
        citizen_id: str,
        worker_id: str
    ) -> bool:
        """Notify citizen and worker when complaint is approved"""
        try:
            citizen_msg = "Your complaint has been successfully resolved and closed"
            worker_msg = "Your work has been approved and the complaint is now closed"
            
            if self.email_service:
                await self.email_service.send_completion_notification(
                    citizen_id,
                    "Complaint Resolved",
                    citizen_msg
                )
                await self.email_service.send_completion_notification(
                    worker_id,
                    "Work Approved",
                    worker_msg
                )
            
            if self.notification_repo:
                for user_id, msg in [(citizen_id, citizen_msg), (worker_id, worker_msg)]:
                    await self.notification_repo.create({
                        "user_id": user_id,
                        "complaint_id": complaint_id,
                        "type": NotificationType.EMAIL,
                        "title": "Complaint Approved",
                        "message": msg,
                        "status": NotificationStatus.SENT,
                        "created_at": datetime.utcnow()
                    })
            
            logger.info(f"Approval notification sent to citizen {citizen_id} and worker {worker_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending approval notification: {str(e)}")
            return False

    async def notify_complaint_rejected(
        self,
        complaint_id: str,
        worker_id: str,
        reason: str
    ) -> bool:
        """Notify worker when complaint is rejected"""
        try:
            title = "Work Rejected"
            message = f"Your work was not approved. Reason: {reason}"
            
            if self.email_service:
                await self.email_service.send_rejection_notification(
                    worker_id,
                    title,
                    message,
                    reason
                )
            
            if self.notification_repo:
                await self.notification_repo.create({
                    "user_id": worker_id,
                    "complaint_id": complaint_id,
                    "type": NotificationType.EMAIL,
                    "title": title,
                    "message": message,
                    "status": NotificationStatus.SENT,
                    "created_at": datetime.utcnow()
                })
            
            logger.info(f"Rejection notification sent to worker {worker_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending rejection notification: {str(e)}")
            return False
