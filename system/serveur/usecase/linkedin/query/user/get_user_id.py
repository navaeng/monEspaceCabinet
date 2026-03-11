from data.database import supabase_client
from fastapi import (
    HTTPException,
    Request,
)


async def get_user_id(request: Request):

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        print("❌ Authentification manquante")
        raise HTTPException(status_code=401)

    token = auth_header.replace("Bearer ", "")

    user_response = supabase_client().auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Authentification invalide")
    current_user_id = user_response.user.id
    print(f"👤 Utilisateur connecté : {current_user_id}")

    return current_user_id
