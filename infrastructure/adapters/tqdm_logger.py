import time
import threading
from tqdm import tqdm
from core.ports.logger_port import Logger


class TQDMLogger(Logger):
    def __init__(self):
        self.lock = threading.Lock()

    def info(self, message: str):
        with self.lock:
            tqdm.write(f"[{time.strftime('%H:%M:%S')}] ℹ️ {message}")

    def sucesso(self, message: str):
        with self.lock:
            tqdm.write(f"[{time.strftime('%H:%M:%S')}] ✅ {message}")

    def erro(self, message: str):
        with self.lock:
            tqdm.write(f"[{time.strftime('%H:%M:%S')}] ❌ {message}")