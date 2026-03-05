from starlette.middleware.cors import CORSMiddleware

from core.app import app


def config_CORS():

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
