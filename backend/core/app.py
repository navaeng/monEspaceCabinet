import os
import threading

from fastapi import FastAPI

from contextlib import asynccontextmanager

from core.USECASE.linkedin.start_auto import start_auto


@asynccontextmanager
async def thread_(app: FastAPI):
    thread = threading.Thread(target=start_auto, daemon=True)
    thread.start()
    print("Lancement de thread pour les lancements automatique...")
    yield


app = FastAPI(title="Endpoint", version="1.0.0", lifespan=thread_)
KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
print(f"KEY: {KEY_SECRET}")
