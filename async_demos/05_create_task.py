"""Демо 05. await подряд — это ПОСЛЕДОВАТЕЛЬНО. Одновременно — create_task / gather / TaskGroup.

Запуск:  python 05_create_task.py   (TaskGroup требует Python 3.11+)
"""
import asyncio
import time


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay) # имитация сетевого запроса
    exit_time = time.time()
    return f"{name} - {exit_time}"


async def sequential() -> None:
    start = time.perf_counter()
    a = await fetch("A", 1)  # ждём A целиком...
    b = await fetch("B", 1)  # ...и только потом начинаем B
    print(f"Два await подряд:     {time.perf_counter() - start:.1f} c  {a}, {b}")


async def with_tasks() -> None:
    start = time.perf_counter()
    task_a = asyncio.create_task(fetch("A", 3))  # A запущена и уже ждёт
    task_b = asyncio.create_task(fetch("B", 1))  # B запущена и уже ждёт
    # ... здесь можно делать другую работу ...
    a = await task_a
    b = await task_b
    print(f"create_task:          {time.perf_counter() - start:.1f} c  {a}, {b}")


async def with_gather() -> None:
    start = time.perf_counter()
    a, b = await asyncio.gather(fetch("A", 1), fetch("B", 1))
    print(f"gather:               {time.perf_counter() - start:.1f} c  {a}, {b}")


async def with_task_group() -> None:
    start = time.perf_counter()
    async with asyncio.TaskGroup() as tg:  # Python 3.11+
        task_a = tg.create_task(fetch("A", 1))
        task_b = tg.create_task(fetch("B", 1))
    # выход из async with = все задачи группы завершены
    print(f"TaskGroup:            {time.perf_counter() - start:.1f} c  {task_a.result()}, {task_b.result()}")


async def main() -> None:
    await sequential()
    await with_tasks()
    await with_gather()
    await with_task_group()


asyncio.run(main())
