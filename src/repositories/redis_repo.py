from loguru import logger

from redis.asyncio import Redis
from redis.exceptions import RedisError

from src.core.repositories.redis_repo import IRedisRepository


class RedisRepository(IRedisRepository):

    def __init__(self, redis_client: Redis):
        self.client = redis_client

    def push(self, obj):
        try:
            self.client.rpush('image_queue', obj)
        except RedisError as e:
            logger.error(e)

    def pop(self):
        try:
            return self.client.lpop('image_queue')
        except RedisError as e:
            logger.error(e)

    def close(self):
        try:
            self.client.close()
        except RedisError as e:
            logger.error(e)
