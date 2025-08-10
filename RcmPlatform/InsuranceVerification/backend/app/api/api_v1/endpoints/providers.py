# File: app/api/api_v1/endpoints/providers.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.crud_provider import provider
from app.schemas.provider import Provider, ProviderCreate, ProviderUpdate
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[Provider])
async def get_providers(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get all providers."""
    try:
        providers = provider.get_multi(db=db, skip=skip, limit=limit)
        return providers
    except Exception as e:
        logger.error(f"Error retrieving providers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve providers"
        )


@router.get("/active", response_model=List[Provider])
async def get_active_providers(*, db: Session = Depends(get_db)) -> Any:
    """Get all active providers."""
    try:
        providers = provider.get_active(db=db)
        return providers
    except Exception as e:
        logger.error(f"Error retrieving active providers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve active providers"
        )


@router.get("/{provider_id}", response_model=Provider)
async def get_provider(*, db: Session = Depends(get_db), provider_id: int) -> Any:
    """Get provider by ID."""
    try:
        db_provider = provider.get(db=db, id=provider_id)
        if not db_provider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider not found"
            )
        return db_provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving provider {provider_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve provider"
        )


@router.get("/npi/{npi}", response_model=Provider)
async def get_provider_by_npi(*, db: Session = Depends(get_db), npi: str) -> Any:
    """Get provider by NPI."""
    try:
        db_provider = provider.get_by_npi(db=db, npi=npi)
        if not db_provider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider not found"
            )
        return db_provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving provider with NPI {npi}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve provider"
        )


@router.post("/", response_model=Provider)
async def create_provider(
    *, db: Session = Depends(get_db), provider_in: ProviderCreate
) -> Any:
    """Create new provider."""
    try:
        # Check if provider with NPI already exists
        existing_provider = provider.get_by_npi(db=db, npi=provider_in.npi)
        if existing_provider:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provider with this NPI already exists"
            )
        
        db_provider = provider.create(db=db, obj_in=provider_in)
        if not db_provider:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create provider"
            )
        return db_provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating provider: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create provider"
        )


@router.put("/{provider_id}", response_model=Provider)
async def update_provider(
    *,
    db: Session = Depends(get_db),
    provider_id: int,
    provider_in: ProviderUpdate
) -> Any:
    """Update provider."""
    try:
        db_provider = provider.get(db=db, id=provider_id)
        if not db_provider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider not found"
            )
        
        updated_provider = provider.update(db=db, db_obj=db_provider, obj_in=provider_in)
        return updated_provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating provider {provider_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update provider"
        )

