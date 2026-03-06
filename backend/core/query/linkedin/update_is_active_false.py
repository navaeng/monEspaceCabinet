from data.database import supabase_client
from core.USECASE.linkedin.classes.object_user_data import object_user_data

def update_is_active_false(data, current_user_id, body):

    user_data = object_user_data(data, current_user_id, body)
    user_id = user_data.get("id")

    if user_id:
        try:
            supabase_client.table("prospection_settings").update(
                {"is_active": False}
            ).eq("id", user_id).execute()

        except Exception as e:
            if "204" not in str(e) and "Missing response" not in str(e):
                print(f"Erreur DB: {e}")
            else:
                print(f"Log technique: {e}")