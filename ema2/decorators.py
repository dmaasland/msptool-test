import asyncio
from functools import lru_cache, wraps
from typing import Awaitable, Callable


def ratelimit(time: int, total: int):
    limit = asyncio.Semaphore(total)

    @lru_cache(maxsize=1)
    def decorator(func: Callable[[int, int], Awaitable[None]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with limit:
                if limit.locked():
                    print("Rate limited..")
                    await asyncio.sleep(60 * time)

                return await func(*args, **kwargs)

        return wrapper

    return decorator
