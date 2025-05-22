import pytest
import os


@pytest.mark.asyncio
async def test_async_batch_ingest_prices(monkeypatch, db_session):
    from app.datapipeline.pipeline import async_batch_ingest_prices

    # Patch httpx.AsyncClient.get
    class DummyResponse:
        def json(self):
            # Simulate a valid API response
            return {
                "results": [
                    {
                        "date": "2023-01-01",
                        "open": 100,
                        "high": 110,
                        "low": 90,
                        "close": 105,
                        "volume": 1000,
                    }
                ]
            }

        def raise_for_status(self):
            pass  # Simulate always OK

    class DummyAsyncClient:
        async def get(self, *args, **kwargs):
            return DummyResponse()

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            # This method is intentionally left empty because no cleanup is needed for the dummy client.
            pass

    monkeypatch.setattr("httpx.AsyncClient", DummyAsyncClient)
    # Patch env keys if used in your code (for Google/OpenAI etc)
    monkeypatch.setenv("FINANCIAL_DATASETS_API_KEY", "FAKE")
    monkeypatch.setenv("GOOGLE_API_KEY", "FAKE")
    monkeypatch.setenv("FINANCIAL_DATASETS_PRICES_ENDPOINT", "https://example.com")
    monkeypatch.setenv("GOOGLE_GEMINI_EMBEDDINGS_MODEL", "fake-model")

    # Call function with dummy params (make sure params match signature)
    await async_batch_ingest_prices("AAPL", "2023-01-01", "2023-01-02")


@pytest.mark.asyncio
async def test_async_embed_new_records(monkeypatch):
    from app.datapipeline import pipeline
    from app.datapipeline.pipeline import async_embed_new_records

    class DummyEmbeddings:
        def embed_documents(self, docs):
            return [[0.1] * 3072 for _ in docs]

    # Patch embeddings and DB calls as needed for this logic
    pipeline.embeddings = DummyEmbeddings()
    # If your function relies on more, mock those accordingly

    # Run function (should not raise)
    await async_embed_new_records()
