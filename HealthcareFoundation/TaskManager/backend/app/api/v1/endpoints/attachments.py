# app/api/v1/endpoints/attachments.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path

from app import crud, models, schemas
from app.core.database import get_db
from app.core.config import settings
from app.utils.file_utils import validate_file, save_upload_file

router = APIRouter()


@router.post("/upload", response_model=schemas.Attachment)
async def upload_file(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    task_id: Optional[int] = Form(None),
) -> Any:
    """
    Upload a file attachment.
    """
    # Validate file
    if not validate_file(file.filename, file.size):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type or file too large"
        )
    
    # Save file
    file_path = await save_upload_file(file)
    
    # Create attachment record
    attachment_in = schemas.AttachmentCreate(
        file_name=file.filename,
        file_path=file_path,
        file_size=file.size,
        file_type=file.content_type,
        task_id=task_id
    )
    
    attachment = crud.attachment.create(db=db, obj_in=attachment_in)
    return attachment


@router.get("/{attachment_id}", response_model=schemas.Attachment)
def get_attachment(
    *,
    db: Session = Depends(get_db),
    attachment_id: int,
) -> Any:
    """
    Get attachment metadata.
    """
    attachment = crud.attachment.get(db=db, id=attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment


@router.get("/{attachment_id}/download")
def download_attachment(
    *,
    db: Session = Depends(get_db),
    attachment_id: int,
) -> Any:
    """
    Download an attachment file.
    """
    attachment = crud.attachment.get(db=db, id=attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    if not os.path.exists(attachment.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=attachment.file_path,
        filename=attachment.file_name,
        media_type="application/octet-stream"
    )


@router.delete("/{attachment_id}")
def delete_attachment(
    *,
    db: Session = Depends(get_db),
    attachment_id: int,
) -> Any:
    """
    Delete an attachment.
    """
    attachment = crud.attachment.get(db=db, id=attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    crud.attachment.remove_with_file(db=db, id=attachment_id)
    return {"message": "Attachment deleted successfully"}


@router.get("/task/{task_id}/", response_model=List[schemas.Attachment])
def get_task_attachments(
    *,
    db: Session = Depends(get_db),
    task_id: int,
) -> Any:
    """
    Get all attachments for a task.
    """
    # Verify task exists
    task = crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return crud.attachment.get_by_task(db=db, task_id=task_id)


@router.put("/{attachment_id}/task/{task_id}", response_model=schemas.Attachment)
def associate_attachment_with_task(
    *,
    db: Session = Depends(get_db),
    attachment_id: int,
    task_id: int,
) -> Any:
    """
    Associate an attachment with a task.
    """
    # Verify both exist
    attachment = crud.attachment.get(db=db, id=attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    task = crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    attachment = crud.attachment.update_task_id(
        db=db, attachment_id=attachment_id, task_id=task_id
    )
    return attachment
