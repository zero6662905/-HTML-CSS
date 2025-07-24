import asyncio
from models.Participant import Note
from settings import Base, async_session, async_engine

async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def insert_data():
    async with async_session() as sess:
        n1 = Note(name="mike", email="mike@example.com", event="octoberfest", age=19)
        n2 = Note(name="kopaka", email="kopaka@example.com", event="lijniye gonki", age=25)

        sess.add_all([n1, n2])
        await sess.commit()

async def main():
    await create_db()
    print("database created")
    await insert_data()
    print("data inserted")

if __name__ == "__main__":
    asyncio.run(main())