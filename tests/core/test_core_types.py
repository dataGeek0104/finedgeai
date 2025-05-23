from app.core.types import HealthCheckResponse
import pytest


@pytest.mark.asyncio
async def test_health_check_response_model():
    model = HealthCheckResponse(message="Test")
    assert model.message == "Test"
