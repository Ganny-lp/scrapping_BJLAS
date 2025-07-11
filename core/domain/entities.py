class Edicao:
    def __init__(self, url: str):
        self.url = url


class Artigo:
    def __init__(self, url_view: str, titulo: str, data_publicacao: str):
        self.url_view = url_view
        self.titulo = titulo
        self.data_publicacao = data_publicacao

    @property
    def url_download(self) -> str:
        return self.url_view.replace("/view/", "/download/")