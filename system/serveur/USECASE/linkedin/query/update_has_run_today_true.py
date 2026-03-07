from system.data import supabase_client


def update_has_run_today_true(job_id):
    supabase_client.table("prospection_settings").update(
        {"is_active": True, "has_run_today": True}
    ).eq("id", job_id).execute()