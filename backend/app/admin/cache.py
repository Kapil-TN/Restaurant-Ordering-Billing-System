import json
import redis
from functools import wraps
from flask import jsonify


def get_redis_client():
    # protocol=2 prevents the client from sending the HELLO 3 command,
    # which older Redis/Memurai versions don't support and causes a
    # ResponseError that was crashing every route.
    try:
        client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True,
            protocol=2,         # RESP2 — safe with all Redis versions
            socket_connect_timeout=1,
        )
        return client
    except Exception:
        return None


redis_client = get_redis_client()

# Catch any Redis error (ConnectionError, ResponseError, TimeoutError, etc.)
_REDIS_ERRORS = (redis.exceptions.RedisError, OSError)


def cache_response(cache_key, expiry_seconds):
    def decorator(route_function):
        @wraps(route_function)
        def wrapper(*args, **kwargs):
            # ── Try to read from cache ─────────────────────────────────
            if redis_client is not None:
                try:
                    cached_value = redis_client.get(cache_key)
                    if cached_value is not None:
                        print(f"[CACHE HIT] {cache_key}")
                        return jsonify(json.loads(cached_value)), 200
                    print(f"[CACHE MISS] {cache_key} — calculating fresh data")
                except _REDIS_ERRORS as e:
                    # Redis is broken/unavailable — fail open, serve live data.
                    print(f"[CACHE SKIP] {cache_key} — Redis error: {e}")
            else:
                print(f"[CACHE SKIP] {cache_key} — no Redis client")

            # ── Run the actual route ───────────────────────────────────
            response, status_code = route_function(*args, **kwargs)

            # ── Try to write result into cache ─────────────────────────
            if redis_client is not None:
                try:
                    response_data = response.get_json()
                    redis_client.setex(cache_key, expiry_seconds, json.dumps(response_data))
                except _REDIS_ERRORS:
                    pass

            return response, status_code
        return wrapper
    return decorator
