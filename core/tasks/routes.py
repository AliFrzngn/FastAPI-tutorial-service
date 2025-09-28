from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from tasks.models import *
from tasks.schemas import *
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List

router = APIRouter(tags=["tasks"],prefix="/todo")

@router.get("/task/", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(completed: bool = Query(None,
    description="Filter tasks by completion status"),
    limit: int = Query(10, gt=0, le=50, description="Limit the number of tasks to return"),
    offset: int = Query(0, ge=0, description="Offset the number of tasks to return"),
    db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter_by(is_completed=completed)
   
    return query.limit(limit).offset(offset).all()

@router.get("/task/{task_id}", response_model=TaskResponseSchema)
async def retrieve_tasks_detail(task_id: int, db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_obj

@router.post("/task/", response_model=TaskResponseSchema)
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.put("/task/{task_id}", response_model=TaskResponseSchema)
async def update_task(request: TaskUpdateSchema, 
task_id: int = Path(..., gt=0), 
db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    for field , value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.delete("/task/{task_id}", status_code=204)
async def delete_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
        task_obj = db.query(TaskModel).filter_by(id=task_id).first()
        if not task_obj:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(task_obj)
        db.commit()
