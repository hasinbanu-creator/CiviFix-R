"""File upload service for AWS S3 and MinIO"""
import logging
import mimetypes
from typing import Optional, List
from io import BytesIO

logger = logging.getLogger(__name__)


class FileUploadService:
    """Service for handling file uploads"""

    # Allowed file types
    ALLOWED_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'
    }
    
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB per file
    MAX_FILES = 5

    def __init__(self, s3_client=None, minio_client=None):
        """Initialize with S3 or MinIO client"""
        self.s3_client = s3_client
        self.minio_client = minio_client

    async def validate_file(
        self,
        filename: str,
        file_size: int
    ) -> tuple[bool, Optional[str]]:
        """Validate file before upload"""
        try:
            # Check file extension
            _, ext = filename.rsplit('.', 1)
            ext_lower = f".{ext.lower()}"
            
            if ext_lower not in self.ALLOWED_EXTENSIONS:
                return False, f"File type not allowed. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
            
            # Check file size
            if file_size > self.MAX_FILE_SIZE:
                return False, f"File size exceeds {self.MAX_FILE_SIZE / (1024*1024):.0f}MB limit"
            
            return True, None
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return False, "File validation failed"

    async def upload_to_s3(
        self,
        file_key: str,
        file_content: bytes,
        bucket: str = "civifix-complaints"
    ) -> tuple[bool, Optional[str]]:
        """Upload file to AWS S3"""
        try:
            if not self.s3_client:
                logger.error("S3 client not initialized")
                return False, "S3 service not available"
            
            self.s3_client.put_object(
                Bucket=bucket,
                Key=file_key,
                Body=file_content,
                ACL='public-read',
                ContentType=mimetypes.guess_type(file_key)[0] or 'application/octet-stream'
            )
            
            # Generate URL
            url = f"https://{bucket}.s3.amazonaws.com/{file_key}"
            
            logger.info(f"File uploaded to S3: {file_key}")
            return True, url
            
        except Exception as e:
            logger.error(f"S3 upload error: {str(e)}")
            return False, str(e)

    async def upload_to_minio(
        self,
        file_key: str,
        file_content: bytes,
        bucket: str = "civifix-complaints"
    ) -> tuple[bool, Optional[str]]:
        """Upload file to MinIO"""
        try:
            if not self.minio_client:
                logger.error("MinIO client not initialized")
                return False, "MinIO service not available"
            
            # Upload file
            self.minio_client.put_object(
                bucket,
                file_key,
                BytesIO(file_content),
                length=len(file_content),
                content_type=mimetypes.guess_type(file_key)[0] or 'application/octet-stream'
            )
            
            # Generate URL
            url = f"http://minio:9000/{bucket}/{file_key}"
            
            logger.info(f"File uploaded to MinIO: {file_key}")
            return True, url
            
        except Exception as e:
            logger.error(f"MinIO upload error: {str(e)}")
            return False, str(e)

    async def upload_complaint_image(
        self,
        complaint_id: str,
        filename: str,
        file_content: bytes,
        image_type: str = "complaint"  # complaint or proof
    ) -> tuple[bool, Optional[str]]:
        """Upload complaint image with proper naming"""
        try:
            # Validate file
            valid, error = await self.validate_file(filename, len(file_content))
            if not valid:
                return False, error
            
            # Generate file key
            import uuid
            from datetime import datetime
            
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            _, ext = filename.rsplit('.', 1)
            
            file_key = f"complaints/{complaint_id}/{image_type}/{timestamp}-{unique_id}.{ext}"
            
            # Upload to available service
            if self.s3_client:
                return await self.upload_to_s3(file_key, file_content)
            elif self.minio_client:
                return await self.upload_to_minio(file_key, file_content)
            else:
                logger.error("No upload service configured")
                return False, "Upload service not configured"
                
        except Exception as e:
            logger.error(f"Complaint image upload error: {str(e)}")
            return False, str(e)

    async def delete_file(
        self,
        file_url: str,
        bucket: str = "civifix-complaints"
    ) -> bool:
        """Delete file from storage"""
        try:
            # Extract file key from URL
            if "s3.amazonaws.com" in file_url:
                file_key = file_url.split(f"{bucket}/")[1]
                if self.s3_client:
                    self.s3_client.delete_object(Bucket=bucket, Key=file_key)
                    logger.info(f"File deleted from S3: {file_key}")
                    return True
                    
            elif "minio" in file_url:
                file_key = file_url.split(f"{bucket}/")[1]
                if self.minio_client:
                    self.minio_client.remove_object(bucket, file_key)
                    logger.info(f"File deleted from MinIO: {file_key}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"File deletion error: {str(e)}")
            return False

    async def compress_image(
        self,
        file_content: bytes,
        target_width: int = 800
    ) -> bytes:
        """Compress image before upload"""
        try:
            from PIL import Image
            
            # Open image
            image = Image.open(BytesIO(file_content))
            
            # Resize if larger than target
            if image.width > target_width:
                ratio = target_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((target_width, new_height), Image.Resampling.LANCZOS)
            
            # Save with compression
            output = BytesIO()
            image.save(output, format='JPEG', quality=80, optimize=True)
            
            return output.getvalue()
            
        except ImportError:
            logger.warning("PIL not installed, skipping compression")
            return file_content
        except Exception as e:
            logger.error(f"Image compression error: {str(e)}")
            return file_content
