from data.database import supabase_client


def get_job_title(title, KEY_SECRET):
    rpc_res = supabase_client.rpc(
        "get_decrypted_settings",
        {"job_title_input": title, "key_input": KEY_SECRET},
    ).execute()
    return rpc_res