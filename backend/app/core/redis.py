"""
Redis configuration and client management
"""
from __future__ import annotations
import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings


redis_client: Redis | None = None


async def init_redis() -> None:
    """Initialize Redis connection pool"""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        # Test connection
        await redis_client.ping()
    except Exception:
        # Redis not available, set to None and continue without Redis
        redis_client = None


async def close_redis() -> None:
    """Close Redis connection pool"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def get_redis() -> Redis | None:
    """Get Redis client instance"""
    if redis_client is None:
        await init_redis()
    return redis_client


async def get_redis_client() -> Redis | None:
    """Dependency for getting Redis client"""
    return await get_redis()