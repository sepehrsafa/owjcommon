import aioredis


class RedisManager:
    def __init__(self, url: str):
        self._url = url
        self._pool = None
        self._redis = None

    async def init_redis(self):
        if not self._pool:
            self._pool = aioredis.ConnectionPool.from_url(self._url)
        if not self._redis:
            self._redis = aioredis.Redis(connection_pool=self._pool)

    async def close_redis(self):
        if self._redis:
            await self._redis.close()
        if self._pool:
            await self._pool.disconnect()

    def __getattr__(self, name):
        """
        This method is a fallback. If an attribute is not found in the current class,
        this method is called. We use it to proxy all unknown method calls to the
        underlying Redis connection.
        """

        def method(*args, **kwargs):
            redis_method = getattr(self._redis, name)
            return redis_method(*args, **kwargs)

        return method
