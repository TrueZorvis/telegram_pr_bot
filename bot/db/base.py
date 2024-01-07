from abc import abstractmethod
from datetime import date, datetime as dt, timedelta

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CleanModel:
    """
        Базовая модель в базе данных
    """
    creation_date = Column(DateTime, default=date.today())
    upd_date = Column(DateTime, onupdate=date.today())

    @property
    def no_upd_time(self) -> timedelta:
        return self.upd_date - dt.now()  # type: ignore


class Model(CleanModel):
    """
        Базовая бизнес-модель в базе данных
    """
    @property
    @abstractmethod
    def stats(self) -> str:
        ...
