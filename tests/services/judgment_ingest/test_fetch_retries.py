import httpx
import pytest

from judgment_ingest.pipeline.fetch import RateLimitedError, with_retries


class _Resp:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


def test_repeated_429_raises_rate_limited_error() -> None:
    def boom() -> None:
        raise httpx.HTTPStatusError(
            "rate limited",
            request=httpx.Request("GET", "https://example.com"),
            response=httpx.Response(429),
        )

    with pytest.raises(RateLimitedError, match="increase the source interval"):
        with_retries(boom, retries=2, rate_limiter=None)
