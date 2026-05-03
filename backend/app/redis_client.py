"""
Redis client for caching and real-time data streaming
"""

import redis.asyncio as redis
from typing import Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Async Redis client wrapper
    """
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = await redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                encoding="utf-8"
            )
            await self.client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis")
    
    async def ping(self):
        """Ping Redis"""
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        return await self.client.ping()
    
    async def get(self, key: str):
        """Get value from Redis"""
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        return await self.client.get(key)
    
    async def set(self, key: str, value: str, ex: int = None):
        """Set value in Redis"""
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        return await self.client.set(key, value, ex=ex or settings.REDIS_CACHE_TTL)
    
    async def delete(self, key: str):
        """Delete key from Redis"""
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        return await self.client.delete(key)
    
    async def publish(self, channel: str, message: str):
        """Publish message to Redis channel"""
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        return await self.client.publish(channel, message)
    
    async def subscribe(self, channel: str):
        """Subscribe to Redis channel"""
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        return await self.client.subscribe(channel)


# Global Redis client instance
redis_client = RedisClient()
