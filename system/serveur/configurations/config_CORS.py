from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def config_CORS(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app = FastAPI()
config_CORS(app)