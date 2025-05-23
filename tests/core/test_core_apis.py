import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    resp = await client.get("/api/v0/health-check")
    assert resp.status_code == 200
    assert resp.json() == {"message": "App is working fine!"}
