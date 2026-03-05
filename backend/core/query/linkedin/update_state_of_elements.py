from data.database import supabase_client


def update_state_of_elements():
    supabase_client.table("prospection_settings").update({"is_active": False}).not_.is_(
        "id", "null"
    )
