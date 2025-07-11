import os
import requests
from requests.adapters import HTTPAdapter

# Configurações de diretório
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "pdfs_prolam")

# Configurações de rede
TIMEOUT = 15
MAX_THREADS = 50
URLS = [
    "https://revistas.usp.br/prolam/issue/archive",
    "https://revistas.usp.br/prolam/issue/archive/2"
]

# Seletores CSS
CSS_SELECTORS = {
    "EDICOES": "div.obj_issue_summary a.title",
    "ARTIGOS": "div.obj_article_summary",
    "TITULO": "h3.title a",
    "PDF_LINK": "a.obj_galley_link.pdf",
    "DATA_PUBLICACAO": "div.published span.value"
}

# Configurações de pool HTTP
def criar_http_client() -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=3)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/pdf",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    })
    return session