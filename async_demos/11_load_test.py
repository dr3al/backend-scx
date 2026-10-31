"""Демо 11. Мини-нагрузочный тест: N одновременных запросов к одному эндпоинту.

Сначала запустите сервер:  python 10_fastapi_app.py
Затем:
    python 11_load_test.py /async 50
    python 11_load_test.py /sync 50
    python 11_load_test.py /async-blocking 5
    python 11_load_test.py /async-to-thread 50
Аргументы: путь (по умолчанию /async) и число запросов (по умолчанию 10).
"""
import asyncio
import sys
import time

import httpx

BASE_URL = "http://127.0.0.1:8008"


async def one_request(client: httpx.AsyncClient, path: str, start: float) -> float:
    response = await client.get(path)
    response.raise_for_status()
    return time.perf_counter() - start


async def main(path: str, n: int) -> None:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=120) as client:
        start = time.perf_counter()
        durations = await asyncio.gather(*(one_request(client, path, start) for _ in range(n)))
    total = time.perf_counter() - start
    durations.sort()
    print(f"{n} одновременных запросов к {path}")
    print(f"  первый ответ через {durations[0]:.1f} c, последний через {durations[-1]:.1f} c")
    print(f"  всего {total:.1f} c, пропускная способность {n / total:.1f} запросов/с")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/async"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    asyncio.run(main(path, n))
