import json
import threading
import time

from loguru import logger

from app.common.image_repository import ImageRepository
from app.common.redis_repository import RedisRepository
from app.fetch_service.minio_repository import MinioRepository

locker = threading.Lock()


class FetchService:

    def __init__(self,
                 minio_repository: MinioRepository,
                 redis_repository: RedisRepository,
                 image_repository: ImageRepository,
                 ):
        self.minio_repository = minio_repository
        self.redis_repository = redis_repository
        self.image_repository = image_repository

    def fetch_and_enqueue_images(self):
        images = self.minio_repository.get_all_objects()

        for image in images:
            with locker:
                image_data = {
                    'name': image.object_name,
                    'size': f'{image.size * 0.001:.2f} KB',
                }
                image_name = image.object_name
                obj = json.dumps(image_data, ensure_ascii=False)
                if not self.image_repository.check_image_exists(image.object_name):
                    self.redis_repository.push('image_queue', obj)
                    logger.info(f'Image {image_name} fetched from MinIo')
                time.sleep(1)

        self.redis_repository.close()
