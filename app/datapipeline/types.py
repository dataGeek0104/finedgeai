from pydantic import BaseModel
from datetime import date


class VectorSearchResponse(BaseModel):
    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float
    distance: float
