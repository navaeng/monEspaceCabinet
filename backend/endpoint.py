from core.app import app

from core.configurations.config_CORS import config_CORS
from routes.root_generate_dossier import router_start_generate_dossier
from routes.root_start_chrome import router_start_chrome
from routes.root_listes import router_listes

config_CORS()

@app.get("/")
async def root():
    return {
        "status": "OK",
    }

app.include_router(router_listes)
app.include_router(router_start_chrome)
app.include_router(router_start_generate_dossier)