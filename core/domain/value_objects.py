import re
import unicodedata

class Slug:
    @staticmethod
    def criar(text: str) -> str:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        return re.sub(r'[\s_-]+', '_', text)[:50]

class DataFormatada:
    @staticmethod
    def criar(data_str: str) -> str:
        try:
            return data_str[:7]  # YYYY-MM
        except:
            match = re.search(r"\d{4}", data_str)
            return match.group(0) if match else "sem_data"