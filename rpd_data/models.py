from sqlalchemy import Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class DimDate(Base):
    __tablename__ = "dim_dates"
    date_key = mapped_column(Integer, primary_key=True, autoincrement=True)
    date = mapped_column(Date, unique=True)
    day = mapped_column(Integer, default=0)
    week = mapped_column(Integer, default=0)
    month = mapped_column(Integer, default=0)
    quarter = mapped_column(Integer, default=0)
    year = mapped_column(Integer, default=0)
    day_of_week = mapped_column(Integer, default=0)
