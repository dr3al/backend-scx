"""Демо 12. Асинхронный стек FastAPI + SQLAlchemy 2.0: роут -> сервис -> репозиторий -> AsyncSession.

Та же архитектура, что вы делали синхронно, но с асинхронным драйвером.
Установка:  pip install fastapi uvicorn "sqlalchemy[asyncio]" aiosqlite
Запуск:     python 12_fastapi_async_db.py   ->  http://127.0.0.1:8000/docs
"""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Драйвер указывается в URL после «+»: aiosqlite для SQLite, asyncpg для PostgreSQL.
DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/tasks"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# ---------- Модель ----------
class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(default=False)


# ---------- Схемы ----------
class TaskCreate(BaseModel):
    title: str


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    done: bool


# ---------- Репозиторий: единственное место, где есть I/O ----------
class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Task]:
        result = await self.session.execute(select(Task))  # запрос к БД -> await
        return list(result.scalars().all())                # разбор результата — не I/O

    async def add(self, title: str) -> Task:
        task = Task(title=title)
        self.session.add(task)              # только запоминает объект — не I/O, без await
        await self.session.commit()         # отправка в БД -> await
        await self.session.refresh(task)    # перечитать из БД -> await
        return task


# ---------- Сервис: бизнес-логика ----------
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_all_tasks(self) -> list[Task]:
        return await self.repository.get_all()

    async def create_task(self, title: str) -> Task:
        return await self.repository.add(title.strip())


# ---------- Зависимости ----------
async def get_session() -> AsyncIterator[AsyncSession]:
    # Одна сессия на один запрос. async with закроет её, когда ответ будет отправлен.
    async with SessionLocal() as session:
        yield session


# Эти две зависимости ничего не ждут и ничего не блокируют, поэтому async def:
# FastAPI выполнит их прямо в цикле событий, без похода в пул потоков.
async def get_task_repository(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)


async def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repository)


# ---------- Приложение ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:  # при старте создаём таблицы
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()                      # при остановке закрываем соединения


app = FastAPI(title="Задачи: асинхронный стек", lifespan=lifespan)


@app.get("/tasks", response_model=list[TaskRead])
async def list_tasks(service: TaskService = Depends(get_task_service)):
    return await service.get_all_tasks()


@app.post("/tasks", response_model=TaskRead, status_code=201)
async def create_task(data: TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create_task(data.title)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
