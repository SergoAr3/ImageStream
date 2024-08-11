from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger
from sqlalchemy.orm import sessionmaker

from app.common.db import Image


class ImageRepository:
    def __init__(self, db: sessionmaker):
        self.db = db

    def check_image_exists(self, title: str):
        try:
            with self.db as session:
                image = session.scalar(select(Image).filter_by(title=title))

                return image
        except SQLAlchemyError as e:
            logger.error(e)

    def save_image(self, image: Image):
        try:
            with self.db as session:
                with session.begin():
                    session.add(image)
        except SQLAlchemyError as e:
            logger.error(e)
