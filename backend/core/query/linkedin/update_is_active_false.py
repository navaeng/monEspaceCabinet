from data.database import supabase_client


def update_is_active_false(config_db):

    config_id = config_db.get("id")
    if config_id:
        try:
            supabase_client.table("prospection_settings").update(
                {"is_active": False}
            ).eq("id", config_id).execute()

        except Exception as e:
            if "204" not in str(e) and "Missing response" not in str(e):
                print(f"Erreur DB: {e}")
            else:
                print(f"Log technique: {e}")