from sqlalchemy.exc import SQLAlchemyError

from loguru import logger
from sqlalchemy.orm import sessionmaker

from src.db.model import Image
from src.core.repositories.image_repo import IImageRepository


class ImageRepository(IImageRepository):
    def __init__(self, db: sessionmaker):
        self.db = db

    def save_image(self, image: Image):
        try:
            with self.db as session:
                with session.begin():
                    session.add(image)
                    # await session.flush()
                    # await session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
