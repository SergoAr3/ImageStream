import datetime
import json
import threading
import time

from loguru import logger

from app.common.db import Image
from app.common.image_repository import ImageRepository
from app.common.redis_repository import RedisRepository

locker = threading.Lock()


class StorageService:

    def __init__(self,
                 image_repository: ImageRepository,
                 redis_repository: RedisRepository):
        self.image_repository = image_repository
        self.redis_repository = redis_repository

    def dequeue_and_save_images(self):
        while True:
            with locker:
                image_data = self.redis_repository.pop('image_queue')
                if image_data is None:
                    break
                image_data = json.loads(image_data)
                image_name = image_data['name']
                image = Image(
                    title=image_name,
                    recording_time=datetime.datetime.now(),
                    size=image_data['size']
                )
                self.image_repository.save_image(image)
                logger.info(f'Image {image_name} saved in DB')
                time.sleep(2)

        self.redis_repository.close()
