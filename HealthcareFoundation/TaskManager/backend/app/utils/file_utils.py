import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.core.config import settings


def validate_file(filename: str, file_size: Optional[int] = None) -> bool:
    """Validate uploaded file"""
    if not filename:
        return False
    
    # Check file extension
    file_extension = get_file_extension(filename)
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        return False
    
    # Check file size
    if file_size and file_size > settings.MAX_FILE_SIZE:
        return False
    
    return True


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return Path(filename).suffix.lower().lstrip('.')


async def save_upload_file(upload_file: UploadFile) -> str:
    """Save uploaded file to disk"""
    # Create uploads directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_FOLDER)
    upload_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    file_extension = get_file_extension(upload_file.filename)
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Save file
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await upload_file.read()
            await f.write(content)
        return str(file_path)
    except Exception as e:
        # Clean up if save failed
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


def delete_file(file_path: str) -> bool:
    """Delete file from disk"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0


def is_safe_path(file_path: str, base_path: str = None) -> bool:
    """Check if file path is safe (prevent directory traversal)"""
    if base_path is None:
        base_path = settings.UPLOAD_FOLDER
    
    try:
        # Resolve the absolute path
        abs_path = os.path.abspath(file_path)
        abs_base = os.path.abspath(base_path)
        
        # Check if the file path is within the base path
        return abs_path.startswith(abs_base)
    except Exception:
        return False
