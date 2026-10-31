"""Демо 09. Тяжёлые вычисления в асинхронной программе — через пул процессов.

Сравниваем: вычисления прямо в корутине (цикл событий замирает) и в ProcessPoolExecutor
(цикл событий продолжает тикать, а вычисления идут на других ядрах).

Запуск:  python 09_cpu_in_process_pool.py
ВАЖНО: блок `if __name__ == "__main__":` обязателен. На Windows и macOS дочерние
процессы заново импортируют этот файл, и без него программа запустит сама себя.
"""
import asyncio
import os
import time
from concurrent.futures import ProcessPoolExecutor

JOBS = [6_000_000] * 4


def heavy_computation(n: int) -> int:
    """Обычная (не async!) функция: чистые вычисления."""
    return sum(i * i for i in range(n))


async def heartbeat(start: float) -> None:
    while True:
        print(f"  [{time.perf_counter() - start:4.1f} c] тик")
        await asyncio.sleep(0.5)


async def in_event_loop() -> None:
    start = time.perf_counter()
    ticker = asyncio.create_task(heartbeat(start))
    await asyncio.sleep(0)  # даём пульсу стартовать
    for n in JOBS:
        heavy_computation(n)  # блокирует цикл: тиков не будет
    print(f"Вычисления в цикле событий: {time.perf_counter() - start:.1f} c")
    ticker.cancel()


async def in_process_pool(pool: ProcessPoolExecutor) -> None:
    loop = asyncio.get_running_loop()
    start = time.perf_counter()
    ticker = asyncio.create_task(heartbeat(start))
    results = await asyncio.gather(
        *(loop.run_in_executor(pool, heavy_computation, n) for n in JOBS)
    )
    print(f"Вычисления в пуле процессов: {time.perf_counter() - start:.1f} c (ядер: {os.cpu_count()})")
    ticker.cancel()


async def main() -> None:
    print("=== 1. Прямо в корутине ===")
    await in_event_loop()
    print("\n=== 2. В пуле процессов ===")
    # Пул создаём ОДИН раз на всё приложение и закрываем через with
    with ProcessPoolExecutor() as pool:
        await in_process_pool(pool)


if __name__ == "__main__":
    asyncio.run(main())
