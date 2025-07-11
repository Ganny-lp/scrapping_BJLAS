from abc import ABC, abstractmethod
from core.domain.entities import Edicao, Artigo


class EdicaoRepository(ABC):
    @abstractmethod
    def obter_todas(self) -> list[Edicao]:
        pass

    @abstractmethod
    def obter_artigos(self, edicao: Edicao) -> list[Artigo]:
        pass


class ArtigoRepository(ABC):
    @abstractmethod
    def salvar(self, artigo: Artigo, response):
        pass