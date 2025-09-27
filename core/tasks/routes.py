from fastapi import APIRouter

router = APIRouter(tags=["tasks"],prefix="/todo")

@router.get("/task/")
async def retrieve_tasks_list():
    return []

@router.get("/task/{task_id}")
async def retrieve_tasks_detail(task_id: int):
    return []