import os

import dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME = os.getenv("DATABASE_NAME", "async_db")


    def uri_sqlite(self):
        return f"sqlite+aiosqlite:///{self.DATABASE_NAME}.db"


api_config = DatabaseConfig()


async_engine: AsyncEngine = create_async_engine(api_config.uri_sqlite(), echo=True)
async_session = async_sessionmaker(bind=async_engine)



class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with async_session() as session:
        yield session
