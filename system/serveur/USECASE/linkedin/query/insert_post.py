from system.data import supabase_client


def insert_post(current_user_id, body):
    try:
        supabase_client.table("posts").upsert(
            {
                "user_id": current_user_id,
                "instruction_post": body.post,
            },
            on_conflict="user_id",
        ).execute()
        print("✅ POST INSERTE dans la table POSTS")
    except Exception as e:
        print(f" ERREUR SUPABASE INSERT DANS LA TABLE POSTS : {e}")
