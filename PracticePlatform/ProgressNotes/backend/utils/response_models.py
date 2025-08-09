from pydantic import BaseModel
from typing import Any, Optional, List, Dict

class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[List[str]] = None

class ErrorResponse(BaseModel):
    """Standard error response model."""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
class PaginatedAPIResponse(APIResponse):
    """Paginated API response model."""
    meta: Optional[PaginationMeta] = None
        
def create_success_response(
    data: Any = None,
    message: str = "Operation successful"
) -> APIResponse:
    """Create a success response."""
    return APIResponse(
        success=True,
        message=message,
        data=data
    )   
        
def create_error_response(
    message: str,
    error_code: str = None,
    details: Dict[str, Any] = None
) -> ErrorResponse:
    """Create an error response."""
    return ErrorResponse(
        success=False,
        message=message,
        error_code=error_code,
        details=details
    )   

