from data.database import supabase_client


def update_is_active_true(user_data):
    job_id = user_data.get("id")
    print(f"id de job : {job_id}")

    if job_id:
        try:
            supabase_client().table("prospection_settings").update(
                {"is_active": True}
            ).eq("id", job_id).execute()
            print(f"✅ Statut mis a jour pour {job_id}")

        except Exception as e:
            if "204" not in str(e) and "Missing response" not in str(e):
                print(f"Erreur DB: {e}")

