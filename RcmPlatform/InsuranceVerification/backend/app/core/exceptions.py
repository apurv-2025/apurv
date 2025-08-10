# File: app/core/exceptions.py
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    """Custom HTTP exception with additional context."""
    
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code
        self.context = context or {}


class ValidationException(DetailedHTTPException):
    """Exception for validation errors."""
    
    def __init__(self, detail: str, field: str = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR",
            context={"field": field} if field else {}
        )


class FileProcessingException(DetailedHTTPException):
    """Exception for file processing errors."""
    
    def __init__(self, detail: str, file_type: str = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="FILE_PROCESSING_ERROR",
            context={"file_type": file_type} if file_type else {}
        )


class OCRException(DetailedHTTPException):
    """Exception for OCR processing errors."""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="OCR_ERROR"
        )


class EDIException(DetailedHTTPException):
    """Exception for EDI processing errors."""
    
    def __init__(self, detail: str, transaction_type: str = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="EDI_ERROR",
            context={"transaction_type": transaction_type} if transaction_type else {}
        )


class EligibilityException(DetailedHTTPException):
    """Exception for eligibility verification errors."""
    
    def __init__(self, detail: str, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="ELIGIBILITY_ERROR",
            context={"request_id": request_id} if request_id else {}
        )
