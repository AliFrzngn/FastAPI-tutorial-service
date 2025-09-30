from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes


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


app = FastAPI(
    title="todo app",
    description="learning how to code",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ali Farzanegan",
        "url": "https://google.com",
        "email": "example@gmail.com",
    },
    license_info={
        "name": "MIT"}
        ,lifespan=lifespan, openapi_tags=tags_metadata)

app.include_router(tasks_routes, prefix="/api/v1")
app.include_router(users_routes, prefix="/api/v1")