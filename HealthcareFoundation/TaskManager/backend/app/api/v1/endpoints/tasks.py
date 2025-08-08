from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app import crud, models, schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    overdue: Optional[bool] = Query(None),
    due_date: Optional[date] = Query(None),
    search: Optional[str] = Query(None),
) -> Any:
    """
    Retrieve tasks with optional filtering.
    """
    tasks = crud.task.get_filtered(
        db=db,
        status=status,
        priority=priority,
        client_id=client_id,
        overdue=overdue,
        due_date=due_date,
        search=search,
        skip=skip,
        limit=limit
    )
    return tasks


@router.post("/", response_model=schemas.Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: schemas.TaskCreate,
) -> Any:
    """
    Create new task.
    """
    task = crud.task.create(db=db, obj_in=task_in)
    return task


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
) -> Any:
    """
    Get task by ID.
    """
    task = crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: schemas.TaskUpdate,
) -> Any:
    """
    Update a task.
    """
    task = crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = crud.task.update(db=db, db_obj=task, obj_in=task_in)
    return task


@router.delete("/{task_id}")
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
) -> Any:
    """
    Delete a task.
    """
    task = crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.task.remove(db=db, id=task_id)
    return {"message": "Task deleted successfully"}


@router.get("/stats/overview", response_model=schemas.TaskStats)
def get_task_stats(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get task statistics.
    """
    return crud.task.get_stats(db=db)


@router.get("/overdue/", response_model=List[schemas.Task])
def get_overdue_tasks(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get overdue tasks.
    """
    return crud.task.get_overdue(db=db)


@router.get("/due-today/", response_model=List[schemas.Task])
def get_due_today_tasks(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get tasks due today.
    """
    return crud.task.get_due_today(db=db)
