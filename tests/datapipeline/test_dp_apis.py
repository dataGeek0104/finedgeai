import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ticker, start, end, expected_status",
    [
        ("AAPL", "2023-01-01", "2023-01-10", 200),
        ("FAKE", "2023-01-01", "2023-01-02", 200),
        ("", "2023-01-01", "2023-01-02", 404),  # missing ticker
        ("AAPL", "", "2023-01-02", 200),  # missing start
        ("AAPL", "bad-date", "2023-01-02", 200),  # bad start date
    ],
)
async def test_api_batch_ingest(
    monkeypatch, client, ticker, start, end, expected_status
):
    # Mock the pipeline function so no real API/db call is made
    from app.datapipeline import apis as dp_apis

    async def dummy_batch_ingest_prices(ticker, start, end, **kwargs):
        return None

    monkeypatch.setattr(dp_apis, "async_batch_ingest_prices", dummy_batch_ingest_prices)

    url = f"/api/v0/pipeline/batch/{ticker}?start={start}&end={end}"
    resp = await client.get(url)
    assert resp.status_code == expected_status


@pytest.mark.asyncio
async def test_api_embed(monkeypatch, client):
    from app.datapipeline import apis as dp_apis

    async def dummy_embed():
        return None

    monkeypatch.setattr(dp_apis, "async_embed_new_records", dummy_embed)
    resp = await client.patch("/api/v0/pipeline/embed")
    assert resp.status_code == 200
    assert resp.json()["status"] == "embeddings_updated"
