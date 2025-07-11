import time

from core.application.services import ScrapingService
from infrastructure.config import criar_http_client, DOWNLOAD_DIR, MAX_THREADS
from infrastructure.adapters.http_edicao_repository import HTTPEdicaoRepository
from infrastructure.adapters.file_artigo_repository import FileArtigoRepository
from infrastructure.adapters.tqdm_logger import TQDMLogger
import os


def main():
    start_time = time.perf_counter()
    logger = TQDMLogger()

    try:
        # Configurar ambiente
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        http_client = criar_http_client()

        # Injetar dependências
        service = ScrapingService(
            edicao_repo=HTTPEdicaoRepository(http_client),
            artigo_repo=FileArtigoRepository(),
            http_client=http_client,
            logger=logger,
            max_threads=MAX_THREADS
        )

        # Executar pipeline
        resultado = service.executar()

        # Relatório final
        elapsed = time.perf_counter() - start_time
        logger.info("\n" + "=" * 60)
        logger.info("🏁 RELATÓRIO FINAL")
        logger.info(f"• Edições processadas: {resultado['edicoes']}")
        logger.info(f"• Artigos encontrados: {resultado['artigos']}")
        logger.info(f"• Downloads bem-sucedidos: {resultado['sucessos']}")
        logger.info(f"• Tempo total: {elapsed:.2f} segundos")
        logger.info(f"• Velocidade: {resultado['artigos'] / max(elapsed, 0.1):.1f} artigos/segundo")
        logger.info("=" * 60)

    except Exception as e:
        logger.erro(f"Erro fatal: {str(e)}")
    finally:
        logger.info("Execução concluída")


if __name__ == "__main__":
    main()