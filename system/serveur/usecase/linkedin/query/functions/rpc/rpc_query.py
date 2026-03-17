import os

from data.database import supabase_client


def rpc_query(user_data):
    KEY_SECRET = os.getenv("ENCRYPTION_SECRET")

    rpc_res = supabase_client().rpc(
        "get_decrypted_settings",
        {
            "job_title_input": user_data.get("job_title"),
            "user_id_input": user_data.get("user_id"),
            "key_input": KEY_SECRET
        }
    ).execute()

    return rpc_res