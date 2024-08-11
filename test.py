import redis.asyncio

from app.common.config.settings import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


l = r.lrange('image_queue', 0, 5)

name = 'aff'.encode('utf-8')

print(name in l)
