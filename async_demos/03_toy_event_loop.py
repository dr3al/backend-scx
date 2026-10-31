"""Демо 03. Игрушечный цикл событий на 40 строк — как asyncio устроен внутри.

Это НЕ asyncio, но корутины здесь настоящие, написанные через async def / await.
Идея та же, что и в настоящем цикле:
  1) корутина работает до первого await и «отдаёт» циклу заявку (здесь — Sleep);
  2) цикл откладывает её до момента, когда заявка выполнена;
  3) пока корутина ждёт, цикл выполняет другие корутины.

Запуск:  python 03_toy_event_loop.py
"""
import heapq
import time
from collections import deque


class Sleep:
    """Awaitable-объект: «разбуди меня через seconds секунд»."""

    def __init__(self, seconds: float):
        self.seconds = seconds

    def __await__(self):
        yield self  # отдаём заявку циклу и замираем здесь до следующего send()


class ToyEventLoop:
    def __init__(self):
        self.ready = deque()  # корутины, которые можно выполнять прямо сейчас
        self.sleeping = []    # куча: (время пробуждения, порядковый номер, корутина)
        self.counter = 0

    def create_task(self, coro):
        self.ready.append(coro)

    def run(self):
        while self.ready or self.sleeping:
            # 1. Будим всех, чьё время пришло
            now = time.monotonic()
            while self.sleeping and self.sleeping[0][0] <= now:
                _, _, coro = heapq.heappop(self.sleeping)
                self.ready.append(coro)

            # 2. Работать некому — ждём ближайшего пробуждения.
            #    Настоящий asyncio здесь ждёт не через sleep, а через select/epoll:
            #    «разбуди меня, когда придут данные в любой из сокетов или выйдет таймаут».
            if not self.ready:
                time.sleep(self.sleeping[0][0] - now)
                continue

            # 3. Даём одной корутине поработать до её следующего await
            coro = self.ready.popleft()
            try:
                request = coro.send(None)
            except StopIteration as stop:
                print(f"{stamp()}   [цикл] корутина завершилась, результат: {stop.value!r}")
                continue

            # 4. Корутина приостановилась и отдала заявку — кладём её «спать»
            if isinstance(request, Sleep):
                self.counter += 1
                wake_at = time.monotonic() + request.seconds
                heapq.heappush(self.sleeping, (wake_at, self.counter, coro))


START = time.monotonic()


def stamp() -> str:
    return f"[{time.monotonic() - START:3.1f} c]"


async def worker(name: str, delay: float) -> str:
    print(f"{stamp()} {name}: начал работу, жду {delay} c")
    await Sleep(delay)
    print(f"{stamp()} {name}: проснулся, заканчиваю")
    return f"готово {name}"


if __name__ == "__main__":
    loop = ToyEventLoop()
    loop.create_task(worker("A", 2))
    loop.create_task(worker("B", 1))
    loop.create_task(worker("C", 3))
    loop.run()
    print(f"{stamp()} Всего прошло ≈ 3 c, а не 2 + 1 + 3 = 6 c")
