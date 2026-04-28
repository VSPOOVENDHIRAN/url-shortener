import string

BASE62 = string.ascii_letters + string.digits

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]

    result = []
    base = len(BASE62)

    while num > 0:
        result.append(BASE62[num % base])
        num //= base

    return "".join(reversed(result))

from fastapi import HTTPException
from .redis_client import redis_client
from collections import defaultdict
import time

rate_limit_store = defaultdict(list)

def check_rate_limit(request):
    ip = request.client.host
    key = f"rate_limit:{ip}"
    print(f"Checking rate limit for IP: {ip}")
    # 🔹 Try Redis first
    try:
        if redis_client:
            current = redis_client.get(key)

            if current and int(current) > 10:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )

            redis_client.incr(key)
            redis_client.expire(key, 60)
            return

    except Exception:
        print(" Redis not available → using fallback")
    print("ddddddddd")
    # 🔹 Fallback (in-memory)
    now = time.time()
    window = 60
    now = time.time()

    # clean old requests
    rate_limit_store[ip] = [
        t for t in rate_limit_store[ip] if now - t < window
    ]
    print(f"Rate limit check for IP: {ip}, Requests in window: {len(rate_limit_store[ip])}")

    if len(rate_limit_store[ip]) >= 10:
        oldest = rate_limit_store[ip][0]   #  first request in window
        remaining = int(window - (now - oldest))

        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers={"Retry-After": str(max(1, remaining))}
        )
    rate_limit_store[ip].append(now)


from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def normalize_url(url: str) -> str:
    url = url.strip()

    # add https if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    # sort query params (important)
    query = parse_qs(parsed.query)
    sorted_query = urlencode(sorted(query.items()), doseq=True)

    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path.rstrip("/"),
        "",
        sorted_query,
        ""
    ))

    return normalized