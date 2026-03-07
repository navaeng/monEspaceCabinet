from data.database import supabase_client


def get_linkedin_contacts(current_user_id):
    try:
        contacts_res = (
            supabase_client.table("linkedin_contacts")
            .select("profile_url, origin_mode")
            .eq("user_id", current_user_id)
            .execute()
        )

    except Exception as e:
        print(f"[WARN] Erreur récupération linkedin_contacts: {e}")

    return contacts_res