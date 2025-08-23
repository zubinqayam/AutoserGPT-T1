
import time
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
        async def wrapper(*args, **kwargs):
            req = None
            for a in args:
                if isinstance(a, Request):
                    req = a
                    break
            if req is None:
                req = kwargs.get("request", None)
            if req is None:
                return await func(*args, **kwargs)

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
            return await func(*args, **kwargs)
        return wrapper
    return decorator
