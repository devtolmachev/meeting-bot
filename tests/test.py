import asyncio

from sqlalchemy import select, insert

from src.database._base import Database, Users


async def main():
    query = select(Users)
    db = Database()
    data = await db.fetch(query)
    # print(data)
    db = Database('postgresql+asyncpg://postgres:132671@185.233.187.8:5432/meeting_bot')
    query = insert(Users).values(data)
    await db.execute(query)


if __name__ == '__main__':
    asyncio.run(main())
