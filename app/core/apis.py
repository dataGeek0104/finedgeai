from fastapi import APIRouter
from .types import HealthCheckResponse

tags = ["Root"]
core_router = APIRouter(tags=tags)


@core_router.get(
    "/health-check",
    response_model=HealthCheckResponse,
    description="Checking health of the application.",
    tags=["Root"],
)
async def health_check():
    return HealthCheckResponse(message="App is working fine!")
