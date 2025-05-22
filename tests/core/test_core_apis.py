def test_health_check(client):
    resp = client.get("/api/v0/health-check")
    assert resp.status_code == 200
    assert resp.json() == {"message": "App is working fine!"}
