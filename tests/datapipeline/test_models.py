import pytest
from datetime import date
from uuid import uuid4
from app.datapipeline.models import StockPrice


@pytest.mark.asyncio
async def test_stock_price_insert(db_session):
    stock = StockPrice(
        id=uuid4(),
        ticker="AAPL",
        date=date(2023, 1, 1),
        open=100,
        high=110,
        low=90,
        close=105,
        volume=1000,
        embedding=None,
    )
    db_session.add(stock)
    await db_session.commit()

    # Query back using SQLAlchemy ORM
    result = await db_session.execute(
        StockPrice.__table__.select().where(StockPrice.ticker == "AAPL")
    )
    row = result.fetchone()
    assert row is not None
