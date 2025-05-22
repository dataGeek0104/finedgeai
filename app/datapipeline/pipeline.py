import os
import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import httpx
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.utilities.financial_datasets import FinancialDatasetsAPIWrapper
from sqlalchemy import select

from .init_db import AsyncSessionLocal
from .models import StockPrice

FD_KEY = os.getenv("FINANCIAL_DATASETS_API_KEY")
GG_KEY = os.getenv("GOOGLE_API_KEY")
PRICES_ENDPOINT = (
    os.getenv("FINANCIAL_DATASETS_PRICES_ENDPOINT")
    .encode("utf-8")
    .decode("unicode_escape")
)

fd_wrapper = FinancialDatasetsAPIWrapper(financial_datasets_api_key=FD_KEY)
embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GOOGLE_GEMINI_EMBEDDINGS_MODEL")
)


async def async_batch_ingest_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
):
    headers = {"X-API-KEY": FD_KEY}
    params = {
        "ticker": ticker,
        "interval": interval,
        "interval_multiplier": interval_multiplier,
        "start_date": start_date,
        "end_date": end_date,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(PRICES_ENDPOINT, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json().get("prices", [])

    async with AsyncSessionLocal() as session:
        async with session.begin():
            for r in data:
                record = StockPrice(
                    id=uuid4(),
                    ticker=ticker,
                    date=datetime.fromisoformat(str(r["time"]).split("T")[0]).date(),
                    open=r["open"],
                    high=r["high"],
                    low=r["low"],
                    close=r["close"],
                    volume=r["volume"],
                )
                session.add(record)


async def async_embed_new_records():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(StockPrice).filter(StockPrice.embedding.is_(None))
        )
        rows = result.scalars().all()

        for r in rows:
            text = (
                f"{r.ticker} on {r.date}: "
                f"open {r.open}, close {r.close}, "
                f"high {r.high}, low {r.low}, vol {r.volume}"
            )
            vector = await embeddings.aembed_query(text)
            r.embedding = vector

        await session.commit()


async def streaming_stub(ticker: str, poll_interval_sec: int = 60):
    """A simple async polling loop stub."""
    while True:
        # In real life, swap for a websocket or message-broker client
        await async_batch_ingest_prices(
            ticker,
            start_date=(datetime.now(datetime.timezone.utc) - timedelta(days=1))
            .date()
            .isoformat(),
            end_date=datetime.now(datetime.timezone.utc).date().isoformat(),
            interval="minute",
        )
        await async_embed_new_records()
        await asyncio.sleep(poll_interval_sec)
