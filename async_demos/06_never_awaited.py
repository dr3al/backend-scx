"""Демо 06. Самая частая ошибка новичка: забытый await.

Запуск:  python 06_never_awaited.py
Смотрите на две вещи: AttributeError и предупреждение RuntimeWarning.
"""
import asyncio


class User:
    def __init__(self, name: str):
        self.name = name


async def get_user() -> User:
    await asyncio.sleep(0.1)  # имитация запроса к БД
    return User("Алиса")


async def process_wrong() -> None:
    user = get_user()  # ОШИБКА: забыли await — в user лежит корутина, а не пользователь
    print("Что лежит в user:", user)
    print(user.name)   # у корутины нет атрибута name -> AttributeError


async def process_right() -> None:
    user = await get_user()  # дождались результата
    print("Что лежит в user:", user)
    print("Имя:", user.name)


async def main() -> None:
    print("=== Без await ===")
    try:
        await process_wrong()
    except AttributeError as error:
        print("AttributeError:", error)

    print("\n=== С await ===")
    await process_right()


asyncio.run(main())
# Предупреждение «coroutine 'get_user' was never awaited» Python печатает тогда,
# когда невыполненная корутина удаляется из памяти, поэтому оно может появиться
# не сразу, а позже в выводе (например, в самом конце).
