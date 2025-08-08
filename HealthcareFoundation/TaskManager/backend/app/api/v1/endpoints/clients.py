from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Client])
def read_clients(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
) -> Any:
    """
    Retrieve clients.
    """
    if search:
        clients = crud.client.search(db=db, query=search, skip=skip, limit=limit)
    else:
        clients = crud.client.get_multi(db=db, skip=skip, limit=limit)
    return clients


@router.post("/", response_model=schemas.Client)
def create_client(
    *,
    db: Session = Depends(get_db),
    client_in: schemas.ClientCreate,
) -> Any:
    """
    Create new client.
    """
    # Check if client with email already exists
    if client_in.email:
        existing_client = crud.client.get_by_email(db=db, email=client_in.email)
        if existing_client:
            raise HTTPException(
                status_code=400,
                detail="Client with this email already exists"
            )
    
    client = crud.client.create(db=db, obj_in=client_in)
    return client


@router.get("/{client_id}", response_model=schemas.Client)
def read_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
) -> Any:
    """
    Get client by ID.
    """
    client = crud.client.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=schemas.Client)
def update_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    client_in: schemas.ClientUpdate,
) -> Any:
    """
    Update a client.
    """
    client = crud.client.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if email is being updated and already exists
    if client_in.email and client_in.email != client.email:
        existing_client = crud.client.get_by_email(db=db, email=client_in.email)
        if existing_client:
            raise HTTPException(
                status_code=400,
                detail="Client with this email already exists"
            )
    
    client = crud.client.update(db=db, db_obj=client, obj_in=client_in)
    return client


@router.delete("/{client_id}")
def delete_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
) -> Any:
    """
    Delete a client.
    """
    client = crud.client.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if client has tasks
    client_tasks = crud.client.get_client_tasks(db=db, client_id=client_id)
    if client_tasks:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete client with existing tasks"
        )
    
    crud.client.remove(db=db, id=client_id)
    return {"message": "Client deleted successfully"}


@router.get("/{client_id}/tasks", response_model=List[schemas.Task])
def get_client_tasks(
    *,
    db: Session = Depends(get_db),
    client_id: int,
) -> Any:
    """
    Get all tasks for a specific client.
    """
    client = crud.client.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return crud.client.get_client_tasks(db=db, client_id=client_id)
