from __future__ import annotations

import asyncio

from httpx import AsyncClient, Limits, Timeout

_DEFAULT_TIMEOUT = Timeout(10.0, connect=5.0)
_DEFAULT_LIMITS = Limits(max_connections=100, max_keepalive_connections=50)

_client: AsyncClient | None = None
_lock = asyncio.Lock()


async def get_http_client() -> AsyncClient:
    """Return the process-wide AsyncClient, creating it on first use."""
    global _client
    if _client is None or _client.is_closed:
        async with _lock:
            if _client is None or _client.is_closed:
                _client = AsyncClient(timeout=_DEFAULT_TIMEOUT, limits=_DEFAULT_LIMITS)
    return _client


async def close_http_client() -> None:
    """Close the shared client. Safe to call on shutdown."""
    global _client
    if _client is not None and not _client.is_closed:
        await _client.aclose()
    _client = None