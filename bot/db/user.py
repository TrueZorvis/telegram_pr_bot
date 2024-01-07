from redis.asyncio import Redis
from sqlalchemy import Column, Integer, VARCHAR, select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import relationship, sessionmaker, selectinload

from .base import Base, Model  # type: ignore


class User(Base, Model):
    __tablename__ = 'users'

    # Telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    # EUR
    balance = Column(Integer, default=0)
    locale = Column(VARCHAR(2), default='ru')
    posts = relationship('Post', back_populates="author", lazy=False)

    @property
    def stats(self) -> str:
        return ""

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self) -> str:
        return self.__str__()


async def get_user(user_id: int, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                    .options(selectinload(User.posts))
                    .filter(User.user_id == user_id)  # type: ignore
            )
            return result.scalars().one()


async def create_user(user_id: int, username: str, locale: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username
            )
            try:
                session.add(user)
            except ProgrammingError as e:
                # TODO: add log
                pass


async def is_user_exists(user_id: int, session_maker: sessionmaker, redis: Redis) -> bool:
    res = await redis.get(name='is_user_exists:' + str(user_id))
    if not res:
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(select(User).where(User.user_id == user_id))
                await redis.set(name='is_user_exists:' + str(user_id), value=1 if sql_res else 0)
                return bool(sql_res)
    else:
        return bool(res)
