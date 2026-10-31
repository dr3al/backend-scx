from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config import DB_URL

Base = declarative_base()
engine = create_async_engine(DB_URL)
SessionLocal = async_sessionmaker(bind=engine, autocommit=False)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

async def get_db():
    async with SessionLocal() as session:
        yield session
