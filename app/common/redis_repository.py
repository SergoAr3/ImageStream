from loguru import logger

from redis.asyncio import Redis
from redis.exceptions import RedisError


class RedisRepository:

    def __init__(self, redis_client: Redis):
        self.client = redis_client

    def push(self, queue_name, obj):
        try:
            self.client.rpush(queue_name, obj)
        except RedisError as e:
            logger.error(e)

    def pop(self, queue_name):
        try:
            return self.client.lpop(queue_name)
        except RedisError as e:
            logger.error(e)

    def get_images(self, queue_name):
        return self.client.lrange(queue_name, 0, -1)

    def close(self):
        try:
            self.client.close()
        except RedisError as e:
            logger.error(e)
