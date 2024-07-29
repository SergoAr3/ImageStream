from abc import ABC, abstractmethod


class IRedisRepository(ABC):

    @abstractmethod
    def push(self, obj):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def close(self):
        pass
