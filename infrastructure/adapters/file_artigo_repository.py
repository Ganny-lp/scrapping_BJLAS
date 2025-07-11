import os
from core.domain.entities import Artigo
from core.domain.value_objects import Slug, DataFormatada
from core.domain.repositories import ArtigoRepository
from infrastructure.config import DOWNLOAD_DIR


class FileArtigoRepository(ArtigoRepository):
    def salvar(self, artigo: Artigo, response):
        # Criar caminho usando value objects
        data_formatada = DataFormatada.criar(artigo.data_publicacao)
        slug = Slug.criar(artigo.titulo)

        dir_path = os.path.join(DOWNLOAD_DIR, data_formatada)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"{slug}.pdf")

        # Salvar com streaming
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=16384):
                if chunk:
                    f.write(chunk)