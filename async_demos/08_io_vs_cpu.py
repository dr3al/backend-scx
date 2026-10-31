"""Демо 08. Асинхронность ускоряет ожидание, но не вычисления.

Пять I/O-задач по 1 c (ожидание) и пять CPU-задач по 1 c (вычисления).
Запуск:  python 08_io_vs_cpu.py   (идёт около 6 секунд)
"""
import asyncio
import time

N = 5


async def io_bound(n: int) -> int:
    await asyncio.sleep(1)  # ждём, процессор свободен
    return n


async def cpu_bound(n: int) -> int:
    start = time.perf_counter()
    while time.perf_counter() - start < 1:  # процессор занят всю секунду
        pass
    return n


async def test_io() -> None:
    start = time.perf_counter()
    await asyncio.gather(*(io_bound(i) for i in range(N)))
    print(f"{N} I/O-задач по 1 c:  {time.perf_counter() - start:.1f} c")


async def test_cpu() -> None:
    start = time.perf_counter()
    await asyncio.gather(*(cpu_bound(i) for i in range(N)))
    print(f"{N} CPU-задач по 1 c:  {time.perf_counter() - start:.1f} c")


asyncio.run(test_io())   # ≈ 1 c: все ждут одновременно
asyncio.run(test_cpu())  # ≈ 5 c: внутри cpu_bound нет ни одного await, задачи идут строго по очереди
