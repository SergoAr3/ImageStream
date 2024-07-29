import asyncio
import datetime
import json
import time

from loguru import logger

from src.core.repositories.image_repo import IImageRepository
from src.core.repositories.minio_repo import IMinioRepository
from src.core.repositories.redis_repo import IRedisRepository
from src.db.model import Image


class ImageService:

    def __init__(self,
                 image_repository: IImageRepository,
                 minio_repository: IMinioRepository,
                 redis_repository: IRedisRepository):
        self.image_repository = image_repository
        self.minio_repository = minio_repository
        self.redis_repository = redis_repository

    def fetch_images(self):
        images = self.minio_repository.get_all_objects()
        for image in images:
            image_data = {
                'name': image.object_name,
                'size': f'{image.size * 0.001:.2f} KB',
            }
            image_name = image.object_name
            obj = json.dumps(image_data, ensure_ascii=False)
            self.redis_repository.push(obj)
            logger.info(f'Image {image_name} fetched from MinIo')
            time.sleep(1)
        self.redis_repository.close()

    def get_images(self):
        while True:
            image_data = self.redis_repository.pop()
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
            time.sleep(1)
        self.redis_repository.close()
