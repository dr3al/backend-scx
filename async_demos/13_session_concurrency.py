"""Демо 13. Одна сессия БД — один запрос за раз.

Слайд «три запроса к БД одновременно» верен только если у каждого запроса
своё соединение. Одну AsyncSession нельзя использовать из нескольких корутин сразу.

Установка:  pip install "sqlalchemy[asyncio]" aiosqlite
Запуск:     python 13_session_concurrency.py
"""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///./concurrency_demo.db")
SessionLocal = async_sessionmaker(engine)


async def query_in_new_session(sql: str):
    async with SessionLocal() as session:  # своя сессия -> своё соединение
        result = await session.execute(text(sql))
        return result.scalar()


async def main() -> None:
    print("=== Две корутины, ОДНА сессия ===")
    async with SessionLocal() as session:
        # return_exceptions=True: gather дождётся обеих корутин и вернёт ошибки как значения
        outcomes = await asyncio.gather(
            session.execute(text("SELECT 1")),
            session.execute(text("SELECT 2")),
            return_exceptions=True,
        )
        for outcome in outcomes:
            if isinstance(outcome, Exception):
                print(f"  ошибка -> {type(outcome).__name__}: {outcome}")
            else:
                print(f"  успех  -> {outcome.scalar()}")

    print("\n=== Две корутины, у каждой СВОЯ сессия ===")
    results = await asyncio.gather(
        query_in_new_session("SELECT 1"),
        query_in_new_session("SELECT 2"),
    )
    print("Результаты:", results)
    await engine.dispose()


asyncio.run(main())
