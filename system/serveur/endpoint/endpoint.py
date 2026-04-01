from fastapi import FastAPI
import uvicorn

from APIRouter.router_add_collaborator import router_add_collaborator
from configurations.config_CORS import config_CORS
from usecase.dossier_competences.APIRouter.root_generate_dossier import router_start_generate_dossier
from usecase.process_candidat.APIRouter.start_process import router_start_process

# from usecase.linkedin.APIRouter.root_start_auto import router_start_auto
# from usecase.linkedin.APIRouter.root_start_chrome import router_start_chrome
# from usecase.linkedin.APIRouter.root_listes import router_listes

app = FastAPI()
config_CORS(app)

@app.get("/")
async def root():
    return {
        "status": "OK",
    }

# app.include_router(router_listes)
# app.include_router(router_start_chrome)
app.include_router(router_start_generate_dossier)
# app.include_router(router_start_auto)
app.include_router(router_add_collaborator)
app.include_router(router_start_process)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)