# from database import supabase_client
# from fastapi import APIRouter, HTTPException, Request

# router = APIRouter()


# @router.post("/ajouter")
# async def ajouter_collaborateur(request: Request):
#     """
#     Endpoint pour ajouter un collaborateur à un cabinet.
#     """
#     auth_header = request.headers.get("Authorization")
#     if not auth_header:
#         print("❌ Authentification manquante")
#         raise HTTPException(status_code=401, detail="Authentification manquante")

#     token = auth_header.replace("Bearer ", "")

#     try:
#         user_response = supabase_client.auth.get_user(token)
#         if not user_response or not user_response.user:
#             raise HTTPException(status_code=401, detail="Authentification invalide")
#         current_user_id = user_response.user.id
#         print(f"👤 Utilisateur connecté : {current_user_id}")

#         body = await request.json()
#         email = body.get("email")
#         role = body.get("role", "member")
#         cabinet_id = body.get("cabinet_id")

#         if not email or not cabinet_id:
#             raise HTTPException(status_code=400, detail="Email ou cabinet_id manquant")

#         # Insertion dans la base de données
#         try:
#             result = (
#                 supabase_client.table("collaborateurs")
#                 .insert(
#                     {
#                         "email": email,
#                         "role": role,
#                         "cabinet_id": cabinet_id,
#                         "invited_by": current_user_id,
#                     }
#                 )
#                 .execute()
#             )

#             if result.status_code >= 400:
#                 raise HTTPException(
#                     status_code=500,
#                     detail=f"Erreur lors de l'insertion en base: {result.data}",
#                 )

#             print(f"✅ Collaborateur ajouté : {email}")
#             return {"status": "success", "message": "Collaborateur ajouté avec succès"}

#         except Exception as e:
#             print(f"❌ Erreur lors de l'insertion en base : {e}")
#             raise HTTPException(
#                 status_code=500, detail="Erreur lors de l'ajout du collaborateur"
#             )

#     except Exception as e:
#         print(f"Erreur d'authentification ou autre : {e}")
#         raise HTTPException(status_code=500, detail="Erreur interne du serveur")
