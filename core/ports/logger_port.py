from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def sucesso(self, message: str):
        pass

    @abstractmethod
    def erro(self, message: str):
        pass