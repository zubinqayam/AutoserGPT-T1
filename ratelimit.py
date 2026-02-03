
import time
import functools
import inspect
from typing import Callable, Dict, Tuple
from fastapi import Request
from fastapi.responses import JSONResponse

_STORE: Dict[str, Tuple[float, int]] = {}

def _key(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    ip = fwd or (request.client.host if request.client else "unknown")
    return f"{ip}:{request.url.path}"

def limiter(limit: int = 60, window_sec: int = 60):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            req = None
            for a in args:
                if isinstance(a, Request):
                    req = a
                    break
            if req is None:
                req = kwargs.get("request", None)

            # If no request found (e.g., in tests or direct function calls), execute without rate limiting
            if req is None:
                if inspect.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

            # Apply rate limiting: check window, count requests, and enforce limits
            now = time.time()
            k = _key(req)
            window_start, count = _STORE.get(k, (now, 0))
            if now - window_start >= window_sec:
                window_start, count = now, 0
            if count + 1 > limit:
                retry_after = max(1, int(window_sec - (now - window_start)))
                return JSONResponse(
                    status_code=429,
                    content={"ok": False, "error": "rate_limited", "retry_after_sec": retry_after},
                    headers={"Retry-After": str(retry_after)},
                )
            _STORE[k] = (window_start, count + 1)

            # Call the original function
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
