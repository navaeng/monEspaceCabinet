from data.database import supabase_client


def get_job_id(user_data, cabinet_id):
    result = supabase_client().table("prospection_settings") \
        .select("id") \
        .eq("cabinet_id", cabinet_id) \
        .order("created_at", descending=True) \
        .limit(1).execute()

    if result.data:
        user_data["job_id"] = result.data[0]['id']
    return user_data