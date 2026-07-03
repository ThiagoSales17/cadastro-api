import json

from app.redis_client import get_redis

CACHE_TTL = 30 * 24 * 60 * 60


async def get_cached(key: str) -> dict | None:
    redis = await get_redis()
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None


async def set_cached(key: str, data: dict) -> None:
    redis = await get_redis()
    await redis.setex(key, CACHE_TTL, json.dumps(data))


async def get_or_fetch(key: str, fetch_fn):
    cached = await get_cached(key)
    if cached:
        return cached

    data = await fetch_fn()
    if data:
        await set_cached(key, data)
    return data
