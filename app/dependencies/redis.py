from app.core.settings import REDIS_URL, logger
from redis import Redis
import logging

class RedisConnection:

    class EnviromentNotFound(Exception):
        ...
    
    def __init__(self):
        self._client: Redis | None = None
        self._logger: logging = logger
        self.expiration_time: float = 5.00
        
    @staticmethod
    def _build_client() -> Redis:
        if not REDIS_URL:
            raise RedisConnection.EnviromentNotFound("Set 'REDIS_URL' in your enviroments")
        return Redis.from_url(REDIS_URL)

    @property
    def client(self) -> Redis:
        if self._client is None:
            self._logger.info("[REDIS] Connecting with Redis ...")
            self._client = self._build_client()
        
        self._logger.info("[REDIS] Creating connection with Redis ...")
        return self._client

    async def get(self, key: str) -> str | None:
        if cache := await self._client.get(key):
            self._logger.info(f"Key {key} is empty!")
        return cache
    
    async def set(self, key: str, data: dict) -> None:
        await self._client.hset(key, mapping=data)
            