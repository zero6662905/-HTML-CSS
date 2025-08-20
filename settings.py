import os

import dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME = os.getenv("DATABASE_NAME", "alembic_async_db")

    SECRET_KEY = os.getenv("SECRET_KEY")

    def uri_sqlite(self):
        return f"sqlite+aiosqlite:///{self.DATABASE_NAME}.db"

    def alembic_uri_sqlite(self):
        return f"sqlite:///{self.DATABASE_NAME}.db"


api_config = DatabaseConfig()


# Налаштування бази даних Postgres
# engine = create_engine(api_config.uri_postgres(), echo=True)
async_engine: AsyncEngine = create_async_engine(api_config.uri_sqlite(), echo=True)
async_session = async_sessionmaker(bind=async_engine)


# Декларація базового класу для моделей, Необхідно для реалізації відношень у ORM
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Dependency: сесія БД для FastAPI
async def get_db():
    async with async_session() as session:
        yield session