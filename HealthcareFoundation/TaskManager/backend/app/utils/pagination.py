from typing import Any, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 10
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.per_page
    
    @property
    def limit(self) -> int:
        return self.per_page


class PaginatedResult(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


def paginate(query: Query, params: PaginationParams) -> PaginatedResult:
    """Paginate SQLAlchemy query"""
    total = query.count()
    items = query.offset(params.skip).limit(params.limit).all()
    pages = (total + params.per_page - 1) // params.per_page
    
    return PaginatedResult(
        items=items,
        total=total,
        page=params.page,
        per_page=params.per_page,
        pages=pages,
        has_next=params.page < pages,
        has_prev=params.page > 1
    )

