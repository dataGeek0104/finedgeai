from fastapi import FastAPI, APIRouter
from .types import HealthCheckResponse
from .datapipeline.init_db import init_db
from .datapipeline.apis import pipeline_router, vector_router

# Initialize app globally so uvicorn can discover it
app = FastAPI(
    title="FinEdgeAI",
    version="0.0.0",
    docs_url="/api/v0/docs",
    redoc_url="/api/v0/redoc",
)

api_router = APIRouter(prefix="/api/v0")

app.include_router(pipeline_router)
app.include_router(vector_router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get(
    "/health-check",
    response_model=HealthCheckResponse,
    description="Checking health of the application.",
    tags=["Root"],
)
async def health_check():
    return HealthCheckResponse(
        name=app.title, version=app.version, message="App is working fine!"
    )
