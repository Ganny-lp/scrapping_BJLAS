from abc import ABC, abstractmethod


class LoggerPort(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def success(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass