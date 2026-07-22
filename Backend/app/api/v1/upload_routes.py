from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List, Optional
from pathlib import Path
import os
import re
import uuid
import aiofiles
from app.dependencies.auth_dependency import get_current_user
from app.schemas.user_schema import UserResponseSchema

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]
ASSETS_DIR = BASE_DIR / "assets"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", "heic"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

ASSETS_DIR.mkdir(parents=True, exist_ok=True)

import logging

logger = logging.getLogger(__name__)


def build_user_upload_dir(user_id: str) -> Path:
    """Build a user-scoped asset directory for uploaded images."""
    safe_user_id = re.sub(r"[^A-Za-z0-9._-]+", "-", str(user_id or "user"))
    user_dir = ASSETS_DIR / safe_user_id / "images"
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

@router.post("/", response_model=List[str], summary="Upload multiple images")
async def upload_images(
    files: Optional[List[UploadFile]] = File(None),
    current_user: UserResponseSchema = Depends(get_current_user)
):
    """
    Upload up to 5 images.
    Returns a list of accessible URLs.
    """
    logger.info(f"Upload request received from user: {current_user.get('user_id', 'unknown')}")
    if not files:
        logger.info("No files provided for upload, returning empty list")
        return []
    
    if len(files) > 5:
        logger.error(f"Upload failed: Maximum 5 images allowed, got {len(files)}")
        raise HTTPException(status_code=400, detail="Maximum 5 images allowed")
    
    user_upload_dir = build_user_upload_dir(current_user.get("user_id", "unknown"))
    urls = []
    for file in files:
        filename = file.filename or "image"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File {filename} exceeds 5MB limit")

        new_filename = f"{uuid.uuid4().hex}{ext}"
        filepath = user_upload_dir / new_filename

        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        logger.info(f"Uploaded filename: {new_filename} | path: {filepath}")
        urls.append(f"/assets/{user_upload_dir.relative_to(BASE_DIR).as_posix().split('/', 1)[1]}/{new_filename}")

    logger.info(f"Upload response URLs: {urls}")
    return urls
