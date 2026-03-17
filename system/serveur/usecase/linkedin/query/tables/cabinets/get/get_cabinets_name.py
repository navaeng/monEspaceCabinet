from data.database import supabase_client


def get_cabinets_name(user_data):

    current_user_id = user_data.get("user_id")
    res = (
        supabase_client().table("profiles")
        .select("*, cabinets(nom)")
        .eq("user_id", current_user_id)
        .execute()
    )
    print(f"Supabase response: {res}")

    cabinet_name = ""

    if res.data and len(res.data) > 0:
        first_row = res.data[0]
        if isinstance(first_row, dict):
            cabinet_data = first_row.get("cabinets", {})
            if isinstance(cabinet_data, dict):
                cabinet_name = (
                    str(cabinet_data.get("nom") or "").lower().strip()
                )
                print(f"Cabinet name: {cabinet_name}")

    return cabinet_name