import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from core.domain.entities import Edicao, Artigo
from core.domain.repositories import EdicaoRepository
from infrastructure.config import URLS, CSS_SELECTORS, TIMEOUT


class HTTPEdicaoRepository(EdicaoRepository):
    def __init__(self, session: requests.Session):
        self.session = session

    def obter_todas(self) -> list[Edicao]:
        edicoes = []
        for url_base in URLS:
            response = self.session.get(url_base, timeout=TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            for a in soup.select(CSS_SELECTORS["EDICOES"]):
                if href := a.get('href'):
                    edicoes.append(Edicao(url=urljoin(response.url, href)))
        return edicoes

    def obter_artigos(self, edicao: Edicao) -> list[Artigo]:
        response = self.session.get(edicao.url, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        # Extrair data da edição
        data_publicacao = "sem_data"
        published_div = soup.select_one(CSS_SELECTORS["DATA_PUBLICACAO"])
        if published_div:
            data_publicacao = published_div.get_text(strip=True)

        if published_div:
            value_span = published_div.find("span", class_="value")
            if value_span:
                data_publicacao = value_span.get_text(strip=True)

        artigos = []
        for article in soup.select(CSS_SELECTORS["ARTIGOS"]):
            titulo_tag = article.select_one(CSS_SELECTORS["TITULO"])
            pdf_tag = article.select_one(CSS_SELECTORS["PDF_LINK"])

            if titulo_tag and pdf_tag:
                artigos.append(Artigo(
                    url_view=urljoin(edicao.url, pdf_tag['href']),
                    titulo=titulo_tag.get_text(strip=True),
                    data_publicacao=data_publicacao
                ))
        return artigos