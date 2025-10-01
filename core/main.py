from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from fastapi.middleware.cors import CORSMiddleware
import time
from contextlib import asynccontextmanager
import os

tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to task managment",
        "externalDocs": {
            "description": "More about tasks",
            "url": "https://google.com",
        },
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
    license_info={"name": "MIT"},
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_routes, prefix="/api/v1")
app.include_router(users_routes, prefix="/api/v1")

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Routes for HTML pages
@app.get("/login")
async def login_page():
    return FileResponse(os.path.join(static_path, "login.html"))

@app.get("/dashboard")
async def dashboard_page():
    return FileResponse(os.path.join(static_path, "dashboard.html"))

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_path, "login.html"))


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
