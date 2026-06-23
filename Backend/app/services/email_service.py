"""Email service for sending emails"""

import logging
from email.message import EmailMessage
from typing import Optional

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""

    @staticmethod
    async def send_email(
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send email"""

        try:
            message = EmailMessage()

            message["From"] = settings.SENDER_EMAIL
            message["To"] = to_email
            message["Subject"] = subject

            if html_body:
                message.add_alternative(html_body, subtype="html")
            else:
                message.set_content(body)

            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                start_tls=True,
                username=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD,
            )

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    @staticmethod
    async def send_otp_email(to_email: str, otp: str) -> bool:
        """Send OTP email"""

        subject = "Civifix - OTP Verification"

        body = f"""
Your Civifix OTP verification code is: {otp}

This code will expire in 5 minutes.

If you did not request this code, please ignore this email.

Best regards,
Civifix Team
"""

        return await EmailService.send_email(to_email, subject, body)

    @staticmethod
    async def send_login_otp_email(to_email: str, otp: str) -> bool:
        """Send login OTP email"""

        subject = "Civifix - Login OTP"

        body = f"""
Your Civifix login OTP is: {otp}

This code will expire in 5 minutes.

If you did not request this code, please ignore this email.

Best regards,
Civifix Team
"""

        return await EmailService.send_email(to_email, subject, body)