# tests/test_scraping_service.py
import pytest
from unittest.mock import Mock, create_autospec

from core.application.services import ScrapingService
from core.domain.repositories import EdicaoRepository, ArtigoRepository
from core.ports.logger_port import Logger
from core.domain.entities import Edicao, Artigo
import requests


@pytest.fixture
def artigos():
    return [Artigo(url_view="http://site/view/1", titulo="Artigo 1", data_publicacao="2024-05-01")]

@pytest.fixture
def edicoes():
    return [Edicao(url="http://site/edicao/1")]


def test_executar_retorna_sucesso(edicoes, artigos):
    edicao_repo = create_autospec(EdicaoRepository)
    artigo_repo = create_autospec(ArtigoRepository)
    logger = create_autospec(Logger)
    http_client = create_autospec(requests.Session)

    edicao_repo.obter_todas.return_value = edicoes
    edicao_repo.obter_artigos.return_value = artigos
    http_client.get.return_value = Mock(status_code=200, headers={"Content-Type": "application/pdf"}, iter_content=lambda chunk_size: [b'data'])

    service = ScrapingService(edicao_repo, artigo_repo, http_client, logger)
    resultado = service.executar()

    assert resultado["edicoes"] == 1
    assert resultado["artigos"] == 1
    assert resultado["sucessos"] == 1


def test_falha_em_edicao_nao_aborta_tudo(edicoes):
    edicao_repo = create_autospec(EdicaoRepository)
    artigo_repo = create_autospec(ArtigoRepository)
    logger = create_autospec(Logger)
    http_client = create_autospec(requests.Session)

    edicao_repo.obter_todas.return_value = edicoes
    edicao_repo.obter_artigos.side_effect = Exception("Falha simulada")

    service = ScrapingService(edicao_repo, artigo_repo, http_client, logger)
    resultado = service.executar()

    assert resultado["edicoes"] == 1
    assert resultado["artigos"] == 0
    assert resultado["sucessos"] == 0


def test_nao_salva_se_content_type_invalido(edicoes, artigos):
    edicao_repo = create_autospec(EdicaoRepository)
    artigo_repo = create_autospec(ArtigoRepository)
    logger = create_autospec(Logger)
    http_client = create_autospec(requests.Session)

    edicao_repo.obter_todas.return_value = edicoes
    edicao_repo.obter_artigos.return_value = artigos
    http_client.get.return_value = Mock(status_code=200, headers={"Content-Type": "text/html"})

    service = ScrapingService(edicao_repo, artigo_repo, http_client, logger)
    resultado = service.executar()

    artigo_repo.salvar.assert_not_called()
    assert resultado["sucessos"] == 0
