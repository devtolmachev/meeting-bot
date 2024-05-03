import asyncio
from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import Date, Row, VARCHAR, ARRAY, Integer, BOOLEAN, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from src.etc.database import url_database


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    subscribe_to: Mapped[datetime] = mapped_column(Date, nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    gender_interests: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)
    zodiac_sign: Mapped[str] = mapped_column(nullable=True)
    earn: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[dict] = mapped_column(JSONB, nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    photos_id: Mapped[dict] = mapped_column(JSONB, nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    hide_earn: Mapped[bool] = mapped_column(nullable=True, server_default='false')
    disabled: Mapped[bool] = mapped_column(nullable=True, server_default='false')
    hiden_questionnaire: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, server_default='false')
    cause_hiden_questionnaire: Mapped[str] = mapped_column(nullable=True)
    field_of_activity: Mapped[str] = mapped_column(nullable=True)
    filter_by_distance: Mapped[int] = mapped_column(BigInteger, nullable=True)
    filter_by_age: Mapped[list[int]] = mapped_column(ARRAY(BigInteger), nullable=True)
    filter_by_height: Mapped[list[int]] = mapped_column(ARRAY(BigInteger), nullable=True)
    filter_by_city: Mapped[str] = mapped_column(nullable=True)
    filter_by_activity: Mapped[str] = mapped_column(nullable=True)


class Comunication(Base):
    __tablename__ = "comunications"

    id_row: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    type: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    content: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    from_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    for_id: Mapped[int] = mapped_column(BigInteger, nullable=False)


class Database:
    _engine: AsyncEngine
    session: async_sessionmaker[AsyncSession]
    _database_url: str

    def __init__(self, base_url: str = None):
        if not base_url:
            base_url = url_database
        engine = create_async_engine(url_database, pool_recycle=3600, pool_size=20, max_overflow=0)
        self.session = async_sessionmaker(engine)
        self._engine = engine

    def __await__(self):
        return self._reset_all_tables().__await__()

    async def _reset_all_tables(self):
        async with self._engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        return self

    async def fetchval(self, query: Any) -> Any | None:
        async with self.session() as session:
            res = await session.execute(query)
            try:
                return res.fetchone()[0]
            except TypeError:
                return None

    async def fetchrow(self, query: Any) -> Row[Any] | None:
        async with self.session() as session:
            res = await session.execute(query)
            return res.fetchone()

    async def fetch(self, query: Any) -> Sequence[Row[Any]]:
        async with self.session() as session:
            res = await session.execute(query)
            return res.fetchall()

    async def execute(self, query: Any):
        async with self.session() as session:
            result = await session.execute(query)
            await session.commit()
            return result


def get_db(url: str = None) -> Database:
    if not url:
        url = url_database
    return Database(base_url=url)


async def main():
    ...
    db = Database()
    # await db._reset_all_tables()
    # query = select(Users.photos_id["photo"])

    # query = select(Users.likes)
    # print(query)
    # print(await db.execute(query))


if __name__ == '__main__':
    asyncio.run(main())
