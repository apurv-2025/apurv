from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta, timezone
import asyncio
from enum import Enum

from app.database import SessionLocal, engine, Base
from app.models import Task, TaskExecution
from app.schemas import TaskCreate, TaskResponse, TaskUpdate, TaskExecutionResponse
from app.task_executor import TaskExecutor

app = FastAPI(title="Task Manager API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize task executor
task_executor = TaskExecutor()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Create a new task and schedule it for execution"""
    db_task = Task(
        name=task.name,
        description=task.description,
        task_type=task.task_type,
        payload=task.payload,
        scheduled_time=task.scheduled_time,
        callback_url=task.callback_url,
        max_retries=task.max_retries or 3
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Schedule the task
    if task.scheduled_time <= datetime.now(timezone.utc):
        background_tasks.add_task(task_executor.execute_task, db_task.id)
    else:
        # For future tasks, you'd typically use a job queue like Celery
        background_tasks.add_task(task_executor.schedule_task, db_task.id, task.scheduled_time)
    
    return db_task

@app.get("/api/tasks/", response_model=List[TaskResponse])
def get_tasks(skip: int = 0, limit: int = 100, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all tasks with optional filtering"""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@app.post("/api/tasks/{task_id}/execute")
async def execute_task_now(task_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Execute a task immediately"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    background_tasks.add_task(task_executor.execute_task, task_id)
    return {"message": "Task execution started"}

@app.get("/api/tasks/{task_id}/executions", response_model=List[TaskExecutionResponse])
def get_task_executions(task_id: int, db: Session = Depends(get_db)):
    """Get execution history for a task"""
    executions = db.query(TaskExecution).filter(TaskExecution.task_id == task_id).all()
    return executions

@app.get("/api/executions/", response_model=List[TaskExecutionResponse])
def get_all_executions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all task executions"""
    executions = db.query(TaskExecution).offset(skip).limit(limit).all()
    return executions

# WebSocket endpoint for real-time updates
from fastapi import WebSocket
from typing import Dict
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
