from data.database import supabase_client


def update_is_active_false(user_data):
    user_id = user_data.get("user_id")

    if user_id:
        try:
            supabase_client.table("prospection_settings").update(
                {"is_active": False}
            ).eq("user_id", user_id).execute()
            print(f"✅ Statut désactivé pour l'user {user_id}")

        except Exception as e:
            if "204" not in str(e) and "Missing response" not in str(e):
                print(f"Erreur DB: {e}")