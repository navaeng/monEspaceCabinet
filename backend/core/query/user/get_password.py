from data.database import supabase_client


def get_password(job_title, KEY_SECRET):
    try:
        rpc_res = supabase_client.rpc(
            "get_decrypted_settings",
            {"job_title_input": job_title, "key_input": KEY_SECRET},
        ).execute()
        data = rpc_res.data
        print(f"DEBUG DATA BRUTE: {rpc_res.data}")
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict):
                pass_user = str(first_item.get("linkedin_password", ""))
            else:
                pass_user = ""
        else:
            pass_user = ""
        print(f"Mot de passe récupéré via RPC {pass_user}")
    except Exception as e:
        print(f"❌ Erreur RPC password: {e}")
        yield "Erreur technique lors du décryptage du mot de passe."
        raise e