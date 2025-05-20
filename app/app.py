from fastapi import FastAPI
from .types import HealthCheckResponse

# Initialize app globally so uvicorn can discover it
app = FastAPI(title="FinEdgeAI", version="0.0.0")


@app.get(
    "/",
    response_model=HealthCheckResponse,
    description="Checking health of the application.",
    tags=["Root"],
)
def health_check():
    return HealthCheckResponse(
        name=app.title, version=app.version, message="App is working fine!"
    )
