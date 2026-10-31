"""Демо 01. Три «запроса к БД»: по очереди и одновременно.

Настоящей базы здесь нет: ожидание ответа БД имитируется сном.
  time.sleep(0.1)          — блокирующее ожидание: поток стоит и ничего не делает;
  await asyncio.sleep(0.1) — неблокирующее: корутина отдаёт управление циклу событий.

Запуск:  python 01_sync_vs_async.py
"""
import asyncio
import time


def query_sync(sql: str) -> str:
    time.sleep(0.1)  # ждём «ответа БД» 100 мс, поток заблокирован
    return f"результат {sql!r}"


async def query_async(sql: str) -> str:
    await asyncio.sleep(0.1)  # ждём 100 мс, но не мешаем другим корутинам
    return f"результат {sql!r}"


def run_sync() -> None:
    start = time.perf_counter()
    r1 = query_sync("SELECT * FROM users")     # 100 мс
    r2 = query_sync("SELECT * FROM tasks")     # ещё 100 мс
    r3 = query_sync("SELECT * FROM comments")  # и ещё 100 мс
    print(f"Синхронно:  {time.perf_counter() - start:.2f} c")


async def run_async() -> None:
    start = time.perf_counter()
    # gather запускает все три корутины и ждёт, пока завершатся все
    r1, r2, r3 = await asyncio.gather(
        query_async("SELECT * FROM users"),
        query_async("SELECT * FROM tasks"),
        query_async("SELECT * FROM comments"),
    )
    print(f"Асинхронно: {time.perf_counter() - start:.2f} c")
    print("Результаты пришли в том же порядке, что и запросы:", r1, r2, r3, sep="\n  ")


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())
