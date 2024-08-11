from threading import current_thread

import app.common.config.settings as conf
from app.common.db.database import Session
from app.common.image_repository import ImageRepository

from app.common.redis_repository import RedisRepository
from app.fetch_service.minio_repository import MinioRepository
from app.fetch_service.service import FetchService
from loguru import logger


redis_repo = RedisRepository(conf.REDIS_CLIENT)
minio_repo = MinioRepository(conf.MINIO_CLIENT, conf.MINIO_BUCKET_NAME)
image_repo = ImageRepository(Session())
fetch_service = FetchService(minio_repo, redis_repo, image_repo)


def fetch_and_enqueue_images():
    thread_name = current_thread().name

    try:
        logger.debug(f"Start {thread_name} thread")
        fetch_service.fetch_and_enqueue_images()
        logger.debug(f"Complete {thread_name} task")
    except Exception as e:
        logger.error(f"Error in {thread_name}: {e}")
