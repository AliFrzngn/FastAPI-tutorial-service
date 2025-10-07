from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from fastapi.middleware.cors import CORSMiddleware
import time
from contextlib import asynccontextmanager
import os
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi import BackgroundTasks
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
import httpx
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from core.config import settings
import logging
from utility.email_util import send_email
from core.celery_conf import add_numbers
from celery.result import AsyncResult


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


jobstores = {
    "default": RedisJobStore(jobs_key="apscheduler.jobs",
    run_times_key="apscheduler.run_times",
     host="redis", port=6379, db=1)
}
redis = aioredis.from_url(settings.REDIS_URL)
cache_backend = RedisBackend(redis)
FastAPICache.init(cache_backend, prefix="fastapi-cache")

scheduler = AsyncIOScheduler(jobstores=jobstores)


def my_task():
    logger.info(f"Task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")


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
    scheduler.add_job(my_task, IntervalTrigger(seconds=10), id="my_task", replace_existing=True)
    scheduler.start()
    yield
    scheduler.shutdown()
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

# app.include_router(tasks_routes, prefix="/api/v1")
app.include_router(tasks_routes)
# app.include_router(users_routes, prefix="/api/v1")
app.include_router(users_routes)

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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handelet(request, exc):
    error_response = {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail,
    }
    return JSONResponse(status_code=exc.status_code, content=error_response)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_response = {
        "error": True,
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        "detail": "Problems parsing the request body",
        "content": exc.body,
        "reason": exc.errors,
        "errors": exc.errors(),
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=error_response
    )


def start_task():
    print("Starting task")
    print("Processing...")
    time.sleep(10)
    print("finished task")


@app.get("/initiate-task", status_code=200)
async def initiate_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_task)
    return JSONResponse(content={"message": "Task initiated"})

@app.get("/initiate-celery-task", status_code=200)
async def initiate_celery_task():
    add_numbers.delay(1, 2)
    return JSONResponse(content={"detail": add_numbers.delay(1, 2).id})

@app.get("/check-celery-task-result", status_code=200)
async def check_celery_task(task_id: str):
    result = AsyncResult(task_id).ready()
    return JSONResponse(content={"result": result})


async def request_current_weather(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "current": "temperature_2m,relative_humidity_2m"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current", {})
        return current_weather
    else:
        return None


@app.get("/fetch-current-weather", status_code=200)
@cache(expire=10)
async def fetch_current_weather(latitude: float = 40.7128, longitude: float = -74.0060):
    current_weather = await request_current_weather(latitude, longitude)

    if current_weather:
        return JSONResponse(content={"current_weather": current_weather})
    else:
        return JSONResponse(content={"error": "Failed to fetch current weather"}, status_code=500)


@app.get("/test-send-email", status_code=200)
async def test_send_email():
    await send_email(
        subject="Test Email",
        recipients=["test@example.com"],
        body="This is a test email"
    )
    return JSONResponse(content={"message": "Email sent successfully"})
