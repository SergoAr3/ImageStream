import asyncio
import json

from loguru import logger
from minio import Minio

from src.core.repositories.minio_repo import IMinioRepository


class MinioRepository(IMinioRepository):

    def __init__(self, minio_client: Minio, bucket: str):
        self.client = minio_client
        self.bucket_name = bucket

    def get_object(self, object_name):
        try:
            obj = self.client.get_object(bucket_name=self.bucket_name, object_name=object_name)

            return obj
        except Exception as e:
            logger.error(e)

    def get_all_objects(self):
        try:

            objs = self.client.list_objects(bucket_name=self.bucket_name)
            return [obj for obj in objs]
        except Exception as e:
            logger.error(e)
