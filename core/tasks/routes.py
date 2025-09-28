from fastapi import APIRouter


router = APIRouter(tags=["tasks"],prefix="/todo")

@router.get("/task/")
async def retrieve_tasks_list():
    return []

@router.get("/task/{task_id}")
async def retrieve_tasks_detail(task_id: int):
    return []

@router.post("/task/")
async def create_task():
    return []

@router.put("/task/{task_id}")
async def update_task(task_id: int = Path(..., gt=0):
    return []

@router.delete("/task/{task_id}")
async def delete_task(task_id: int = Path(..., gt=0)):
    return []
