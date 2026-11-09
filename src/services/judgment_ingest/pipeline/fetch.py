"""HTTP fetch helpers: rate limit, retry, 429 backoff."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

import httpx

T = TypeVar("T")


class RateLimiter:
    def __init__(self, min_interval_seconds: float) -> None:
        self.min_interval = min_interval_seconds
        self._last: float | None = None

    def wait(self) -> None:
        now = time.monotonic()
        if self._last is not None:
            elapsed = now - self._last
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
        self._last = time.monotonic()


def with_retries(
    fn: Callable[[], T],
    *,
    retries: int = 3,
    rate_limiter: RateLimiter | None = None,
) -> T:
    last_error: Exception | None = None
    for attempt in range(retries):
        if rate_limiter:
            rate_limiter.wait()
        try:
            return fn()
        except httpx.HTTPStatusError as exc:
            last_error = exc
            if exc.response.status_code == 429:
                time.sleep(2**attempt)
                continue
            if exc.response.status_code >= 500:
                time.sleep(2**attempt)
                continue
            raise
        except httpx.TransportError as exc:
            last_error = exc
            time.sleep(2**attempt)
    assert last_error is not None
    raise last_error
