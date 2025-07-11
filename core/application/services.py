import concurrent.futures
from tqdm import tqdm
from core.ports.repositories import EdicaoRepository, ArtigoRepository
from core.ports.logger_port import Logger
from core.domain.entities import Edicao, Artigo
import requests


class ScrapingService:
    def __init__(
        self,
        edicao_repo: EdicaoRepository,
        artigo_repo: ArtigoRepository,
        http_client: requests.Session,
        logger: Logger,
        max_threads: int = 50
    ):
        self.edicao_repo = edicao_repo
        self.artigo_repo = artigo_repo
        self.http_client = http_client
        self.logger = logger
        self.max_threads = max_threads

    def _processar_edicoes_paralelo(self, edicoes: list[Edicao]) -> list[Artigo]:
        todos_artigos = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, self.max_threads)) as executor:
            futures = {
                executor.submit(self.edicao_repo.obter_artigos, edicao): edicao
                for edicao in edicoes
            }

            for future in tqdm(
                concurrent.futures.as_completed(futures),
                total=len(futures),
                desc="Processando edições",
                unit="edição"
            ):
                try:
                    artigos = future.result()
                    todos_artigos.extend(artigos)
                except Exception as e:
                    edicao = futures[future]
                    self.logger.erro(f"Erro ao processar edição {edicao.url}: {e}")

        return todos_artigos

    def _baixar_artigos_paralelo(self, artigos: list[Artigo]) -> int:
        sucessos = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(self._baixar_artigo, artigo): artigo
                for artigo in artigos
            }

            for future in tqdm(
                concurrent.futures.as_completed(futures),
                total=len(futures),
                desc="Baixando artigos",
                unit="PDF"
            ):
                if future.result():
                    sucessos += 1

        return sucessos

    def _baixar_artigo(self, artigo: Artigo) -> bool:
        try:
            response = self.http_client.get(
                artigo.url_download,
                stream=True,
                timeout=15
            )
            response.raise_for_status()

            if 'application/pdf' not in response.headers.get('Content-Type', ''):
                self.logger.erro(f"Conteúdo inválido para: {artigo.titulo}")
                return False

            self.artigo_repo.salvar(artigo, response)
            self.logger.sucesso(f"PDF salvo: {artigo.titulo}")
            return True

        except Exception as e:
            self.logger.erro(f"Falha no download de '{artigo.titulo}': {str(e)}")
            return False

    def executar(self) -> dict:
        self.logger.info("Iniciando coleta de edições...")
        try:
            edicoes = self.edicao_repo.obter_todas()
        except Exception as e:
            self.logger.erro(f"Erro ao obter edições: {e}")
            return {"edicoes": 0, "artigos": 0, "sucessos": 0}

        self.logger.info(f"Edições encontradas: {len(edicoes)}")

        artigos = self._processar_edicoes_paralelo(edicoes)
        self.logger.info(f"Artigos a serem baixados: {len(artigos)}")

        sucessos = self._baixar_artigos_paralelo(artigos)

        return {
            "edicoes": len(edicoes),
            "artigos": len(artigos),
            "sucessos": sucessos
        }
