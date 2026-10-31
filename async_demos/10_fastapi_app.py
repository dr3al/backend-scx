"""Демо 10 (Демо 3 на паре). Четыре способа «подождать 3 секунды» в FastAPI.

Запуск сервера:   python 10_fastapi_app.py
Потом в другом терминале:  python 11_load_test.py /async 50   (и другие пути)
Документация:     http://127.0.0.1:8000/docs
"""
import asyncio
import time

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Демо: def vs async def")


@app.get("/sync")
def sync_sleep():
    # Обычная функция. FastAPI выполняет её в пуле потоков (по умолчанию до 40 потоков),
    # поэтому блокировка здесь занимает один поток, а не весь сервер.
    time.sleep(3)
    return {"endpoint": "def + time.sleep"}


@app.get("/async")
async def async_sleep():
    # Корутина. Выполняется в цикле событий; на await отдаёт управление,
    # и цикл обслуживает другие запросы.
    await asyncio.sleep(3)
    return {"endpoint": "async def + await asyncio.sleep"}


@app.get("/async-blocking")
async def async_blocking():
    # АНТИПАТТЕРН. Блокирующий вызов внутри async def останавливает цикл событий:
    # сервер не обрабатывает НИКАКИЕ другие запросы, даже /ping.
    time.sleep(3)
    return {"endpoint": "async def + time.sleep (ошибка!)"}


@app.get("/async-to-thread")
async def async_to_thread():
    # Исправление, если блокирующую функцию нельзя заменить:
    # отправляем её в отдельный поток и ждём через await.
    await asyncio.to_thread(time.sleep, 3)
    return {"endpoint": "async def + asyncio.to_thread"}


@app.get("/ping")
async def ping():
    return {"pong": True}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008, log_level="warning")
