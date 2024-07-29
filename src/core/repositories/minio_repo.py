from abc import ABC, abstractmethod


class IMinioRepository(ABC):

    @abstractmethod
    def get_object(self, object_name):
        pass

    @abstractmethod
    def get_all_objects(self):
        pass
