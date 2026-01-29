from typing import Any, Dict, List, cast

from supabase import create_client

from backend.prospection.start_prospection import run_selenium

supabase = create_client("URL", "KEY")


def get_infos_prospect():
    res = (
        supabase.table("prospection_settings")
        .select("*, profiles(linkedin_email, linkedin_password)")
        .eq("is_active", True)
        .execute()
    )

    data_list = cast(list[dict[str, Any]], res.data or [])

    for row in data_list:
        if not isinstance(row, dict):
            continue

        profile = row.get("profiles", {})
        job_title = str(row.get("job_title", ""))

        config_db = {
            "id": row.get("id"),
            "linkedin_email": profile.get("linkedin_email"),
            "linkedin_password": profile.get("linkedin_password"),
            "job_title": job_title,
        }

        print(f" Lancement pour {config_db['linkedin_email']}")
        for update in run_selenium(config_db["job_title"], config_db):
            print(update)
