import threading

from fastapi import FastAPI

from core.USECASE.linkedin.start_auto import start_auto

threading.Thread(target=start_auto, daemon=True).start()

app = FastAPI(title="Endpoint", version="1.0.0")