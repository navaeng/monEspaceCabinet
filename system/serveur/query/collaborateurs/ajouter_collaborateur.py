from pathlib import Path

from dotenv import load_dotenv

from data.get_admin_client import get_admin_client
from data.database import supabase_client
from usecase.linkedin.query.tables.cabinets.get.get_cabinet_id import get_cabinet_id


def query_ajouter_collaborateur(body, cabinet_id):

    try:
            auth_res = get_admin_client().auth.admin.create_user({
                "email": body.email,
                "password": body.password,
            })

            get_admin_client().table("profiles").insert({
                "id": auth_res.user.id,
                "email": body.email,
                "full_name": body.nom,
                "role": body.role,
                "cabinet_id": cabinet_id
            }).execute()
    except Exception as e:
            print(f" ERREUR SUPABASE INSERT DANS LA TABLE profiles : {e}")
