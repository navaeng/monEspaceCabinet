from usecase.linkedin.query.tables.user.get.get_user_data import object_user_data
from serveur.data.database import supabase_client


def check_last_posted():
    user_data = object_user_data()
    res = (
        supabase_client().table("posts")
        .select("id, last_posted_at")
        .eq("user_id", user_data.get("user_id"))
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    return res