from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.mongodb import init_mongodb
from app.routers import package_types, packages, tasks, statistics
from app.tasks.scheduler import start_scheduler
from app.utils.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_mongodb()
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)
configure_logging()

app.include_router(packages.router)
app.include_router(package_types.router)
app.include_router(tasks.router)
app.include_router(statistics.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
