import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


class TimeoutExceeded(Exception):
    pass


async def with_timeout(coro: Awaitable[T], timeout_s: float) -> T:
    try:
        return await asyncio.wait_for(coro, timeout=timeout_s)
    except asyncio.TimeoutError as exc:
        raise TimeoutExceeded(f"Operation exceeded {timeout_s}s timeout") from exc


async def retry_with_backoff(
    fn: Callable[[int], Awaitable[T]],
    max_attempts: int = 4,
    base_delay_s: float = 0.5,
) -> T:
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await fn(attempt)
        except Exception as exc:
            last_error = exc

            if attempt == max_attempts:
                raise

            delay = base_delay_s * (2 ** (attempt - 1))
            jitter = random.uniform(0, 0.1)
            await asyncio.sleep(delay + jitter)

    if last_error is None:
        raise RuntimeError("retry_with_backoff exited without returning or raising")

    raise last_error
