"""Демо 07 (Демо 2 на паре). Блокирующий вызов внутри async def «замораживает» всё.

Фоновая задача heartbeat печатает «тик» каждые 0,5 с — это пульс цикла событий.
Пока пульс есть, цикл может обслуживать другие задачи (в вебе — другие запросы).

Запуск:  python 07_blocking_in_async.py
"""
import asyncio
import time

START = time.perf_counter()


def stamp() -> str:
    return f"[{time.perf_counter() - START:4.1f} c]"


async def heartbeat() -> None:
    while True:
        print(f"{stamp()}   тик — цикл событий свободен")
        await asyncio.sleep(0.5)


async def good_handler() -> None:
    print(f"{stamp()} good: жду 2 c через await asyncio.sleep(2)")
    await asyncio.sleep(2)  # корутина спит, цикл событий свободен
    print(f"{stamp()} good: готово")


async def bad_handler() -> None:
    print(f"{stamp()} bad: жду 2 c через time.sleep(2)  <-- ОШИБКА")
    time.sleep(2)  # блокирует ВЕСЬ поток, а с ним и цикл событий
    print(f"{stamp()} bad: готово")


async def fixed_handler() -> None:
    print(f"{stamp()} fixed: жду 2 c через await asyncio.to_thread(time.sleep, 2)")
    await asyncio.to_thread(time.sleep, 2)  # блокирующий вызов уехал в отдельный поток
    print(f"{stamp()} fixed: готово")


async def scenario(title: str, handler) -> None:
    global START
    START = time.perf_counter()
    print(f"\n=== {title} ===")
    ticker = asyncio.create_task(heartbeat())
    await asyncio.sleep(0.1)  # дадим пульсу начаться
    await handler()
    await asyncio.sleep(0.1)
    ticker.cancel()           # останавливаем фоновую задачу
    try:
        await ticker
    except asyncio.CancelledError:
        pass


async def main() -> None:
    await scenario("1. Неблокирующее ожидание", good_handler)
    await scenario("2. Блокирующее ожидание внутри async def", bad_handler)
    await scenario("3. Исправление через asyncio.to_thread", fixed_handler)


asyncio.run(main())
