from core.app import app

from core.config_CORS import config_CORS
config_CORS()

@app.get("/")
async def root():
    return {
        "message": "L'application tourne !",
        "status": "ok",
        "version": "1.0.0",
    }

from routes.root_listes import router_listes
app.include_router(router_listes)

