# app/vector_apis.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
import openai

from .init_db import AsyncSessionLocal
from .pipeline import async_batch_ingest_prices, async_embed_new_records, embeddings
from .models import StockPrice
from .types import VectorSearchResponse

tags = ["Data Pipeline"]
pipeline_router = APIRouter(prefix="/pipeline", tags=tags)
vector_router = APIRouter(prefix="/vector", tags=tags)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session


@pipeline_router.get("/batch/{ticker}")
async def api_batch_ingest(
    ticker: str,
    start: str = Query(..., description="Provide Start Date in YYYY-MM-DD format"),
    end: str = Query(..., description="Provide End Date in YYYY-MM-DD format"),
):
    try:
        await async_batch_ingest_prices(ticker, start, end)
        return {"status": "ok", "ticker": ticker}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pipeline_router.patch("/embed")
async def api_embed():
    try:
        await async_embed_new_records()
        return {"status": "embeddings_updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@vector_router.get("/search", response_model=list[VectorSearchResponse])
async def vector_search(
    query: str, k: int = Query(5, ge=1, le=20), db: AsyncSession = Depends(get_db)
):
    # compute query embedding
    q_emb = await embeddings.aembed_query(query)

    stmt = (
        select(StockPrice, StockPrice.embedding.cosine_distance(q_emb).label("dist"))
        .order_by("dist")
        .limit(k)
    )
    result = await db.execute(stmt)
    rows = result.all()

    return [
        VectorSearchResponse(
            ticker=row.StockPrice.ticker,
            date=row.StockPrice.date,
            open=row.StockPrice.open,
            high=row.StockPrice.high,
            low=row.StockPrice.low,
            close=row.StockPrice.close,
            volume=row.StockPrice.volume,
            distance=row.dist,
        )
        for row in rows
    ]
