from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from .datapipeline.init_db import init_db
from .datapipeline.apis import pipeline_router, vector_router
from .core.apis import core_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# Initialize app globally so uvicorn can discover it
app = FastAPI(
    title="FinEdgeAI",
    version="0.0.0",
    docs_url="/api/v0/docs",
    redoc_url="/api/v0/redoc",
)

api_router = APIRouter(prefix="/api/v0", lifespan=lifespan)

api_router.include_router(core_router)
api_router.include_router(pipeline_router)
api_router.include_router(vector_router)

app.include_router(api_router)
