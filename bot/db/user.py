from datetime import date

from sqlalchemy import Column, Integer, VARCHAR, DATE

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    # Telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    # Telegram username
    username = Column(VARCHAR(32), unique=False, nullable=True)

    # Registration date
    reg_date = Column(DATE, default=date.today())

    # Last update date
    upd_date = Column(DATE, onupdate=date.today())

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"
