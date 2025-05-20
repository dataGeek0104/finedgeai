from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    name: str
    version: str
    message: str
