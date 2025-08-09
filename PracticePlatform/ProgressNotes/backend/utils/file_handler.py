# backend/utils/file_handler.py
import os
import uuid
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from pathlib import Path
import magic

class FileHandler:
    """Handle file uploads and management."""

    def __init__(self, upload_directory: str = "./uploads", max_size: int = 10 * 1024 * 1024):
        self.upload_directory = Path(upload_directory)
        self.max_size = max_size
        self.allowed_types = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'image/gif',
            'text/plain',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]

        # Create upload directory if it doesn't exist
        self.upload_directory.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile, subfolder: str = "") -> dict:
        """Save uploaded file and return file info."""

        # Validate file size
        content = await file.read()
        if len(content) > self.max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {self.max_size} bytes"
            )

        # Validate file type
        mime_type = magic.from_buffer(content, mime=True)
        if mime_type not in self.allowed_types:
            raise HTTPException(
                status_code=415,
                detail=f"File type {mime_type} not allowed"
            )

        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Create subfolder if specified
        save_directory = self.upload_directory / subfolder if subfolder else self.upload_directory
        save_directory.mkdir(parents=True, exist_ok=True)

        # Save file
        file_path = save_directory / unique_filename
        with open(file_path, "wb") as f:
            f.write(content)

       return {
            "filename": file.filename,
            "saved_filename": unique_filename,
            "file_path": str(file_path),
            "file_size": len(content),
            "mime_type": mime_type
        }

    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                return True
            return False
        except Exception:
            return False

    def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get file information."""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                stat = path.stat()
                return {
                    "filename": path.name,
                    "file_size": stat.st_size,
                    "created_at": stat.st_ctime,
                    "modified_at": stat.st_mtime
                }
            return None
        except Exception:
            return None

