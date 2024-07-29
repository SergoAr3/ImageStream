import redis.asyncio
import src.config as conf

r = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT)

