import time
import threading
from tqdm import tqdm
from core.ports.output_ports import LoggerPort


class TQDMLogger(LoggerPort):
    def __init__(self):
        self.lock = threading.Lock()

    def info(self, message: str):
        with self.lock:
            tqdm.write(f"[{time.strftime('%H:%M:%S')}] ℹ️ {message}")

    def success(self, message: str):
        with self.lock:
            tqdm.write(f"[{time.strftime('%H:%M:%S')}] ✅ {message}")

    def error(self, message: str):
        with self.lock:
            tqdm.write(f"[{time.strftime('%H:%M:%S')}] ❌ {message}")