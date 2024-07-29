from os import getenv

from redis.exceptions import RedisError
from dotenv import load_dotenv

from minio import Minio
from redis import Redis

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

MINIO_ACCESS_KEY = getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = getenv("MINIO_SECRET_KEY")
MINIO_ENDPOINT = getenv("MINIO_ENDPOINT")
MINIO_BUCKET_NAME = getenv("MINIO_BUCKET_NAME")
MINIO_CLIENT = Minio(endpoint=MINIO_ENDPOINT,
                     access_key=MINIO_ACCESS_KEY,
                     secret_key=MINIO_SECRET_KEY,
                     secure=False)

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_CLIENT = Redis(host=REDIS_HOST, port=int(REDIS_PORT), retry_on_error=[RedisError])
