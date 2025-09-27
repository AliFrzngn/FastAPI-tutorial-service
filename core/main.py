from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes


tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to task managment",
        "externalDocs": {
            "description": "More about tasks",
            "url": "https://google.com"
        }
    }
]



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app says hello")
    yield
    print("app says bybye")

app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata)

app.include_router(tasks_routes)