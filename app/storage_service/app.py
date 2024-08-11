from threading import current_thread

import app.common.config.settings as conf
from app.common.db.database import Session
from app.common.image_repository import ImageRepository

from app.common.redis_repository import RedisRepository
from app.storage_service.service import StorageService
from loguru import logger

redis_repo = RedisRepository(conf.REDIS_CLIENT)
image_repo = ImageRepository(Session())
storage_service = StorageService(image_repo, redis_repo)


def dequeue_and_save_images():
    thread_name = current_thread().name

    try:
        logger.debug(f"Start {thread_name} thread")
        storage_service.dequeue_and_save_images()
        logger.debug(f"Complete {thread_name} task")
    except Exception as e:
        logger.error(f"Error in {thread_name}: {e}")
