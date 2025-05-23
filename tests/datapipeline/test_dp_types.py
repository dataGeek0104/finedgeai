from app.datapipeline.types import VectorSearchResponse
from faker import Faker
from datetime import date
import pytest

fake = Faker()


@pytest.mark.asyncio
async def test_vector_search_response_model():
    model = VectorSearchResponse(
        ticker="TEST",
        date=date(1990, 1, 1),
        open=fake.pyfloat(left_digits=3, right_digits=2),
        high=fake.pyfloat(left_digits=3, right_digits=2),
        low=fake.pyfloat(left_digits=3, right_digits=2),
        close=fake.pyfloat(left_digits=3, right_digits=2),
        volume=fake.pyfloat(left_digits=5, right_digits=2),
        distance=fake.pyfloat(left_digits=2, right_digits=5),
    )
    assert isinstance(model, VectorSearchResponse)
    assert model.ticker == "TEST"
