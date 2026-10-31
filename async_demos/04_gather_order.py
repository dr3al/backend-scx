"""Демо 04 (Демо 1 на паре). Три задачи с разными задержками в asyncio.gather.

Запуск:  python 04_gather_order.py
"""
import asyncio
import time

START = time.perf_counter()


def stamp() -> str:
    return f"[{time.perf_counter() - START:3.1f} c]"


async def task(name: str, delay: float) -> str:
    print(f"{stamp()} [{name}] Начало (задержка {delay} c)")
    await asyncio.sleep(delay)
    print(f"{stamp()} [{name}] Завершено")
    return name


async def main() -> None:
    results = await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3),
    )
    # Задачи ЗАВЕРШИЛИСЬ в порядке B, A, C, но gather вернул результаты
    # в порядке, в котором мы их передали: A, B, C.
    print(f"{stamp()} gather вернул: {results}")


asyncio.run(main())
