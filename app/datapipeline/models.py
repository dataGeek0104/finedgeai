from sqlalchemy import Column, UUID, String, Float, Date
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()
SCHEMA_NAME = "finedgeai"


class StockPrice(Base):
    __tablename__ = "stock_prices"
    __table_args__ = {"schema": SCHEMA_NAME}

    id = Column(UUID, primary_key=True, index=True)
    ticker = Column(String, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    embedding = Column(Vector(3072), nullable=True)
