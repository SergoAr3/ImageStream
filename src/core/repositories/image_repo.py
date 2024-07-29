from abc import ABC, abstractmethod

from src.db.model import Image


class IImageRepository(ABC):
    @abstractmethod
    def save_image(self, image: Image):
        pass
