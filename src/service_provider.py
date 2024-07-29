import config.settings as conf

from src.repositories.image_repo import ImageRepository
from src.repositories.minio_repo import MinioRepository
from src.repositories.redis_repo import RedisRepository
from src.core.services.image_service import ImageService
from src.db.database import Session


def get_image_service() -> ImageService:
    redis_repo = RedisRepository(conf.REDIS_CLIENT)
    minio_repo = MinioRepository(conf.MINIO_CLIENT, conf.MINIO_BUCKET_NAME)
    image_repo = ImageRepository(Session())
    image_service = ImageService(image_repo, minio_repo, redis_repo)
    return image_service
