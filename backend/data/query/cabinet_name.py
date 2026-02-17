# # Remplace ton ancien bloc par celui-ci

# user_response = supabase_client.auth.get_user(token)
# current_user_id = user_response.user.id

# res = (
#     supabase_client.table("profiles")
#     .select("*, cabinets(nom)")
#     .eq("id", current_user_id)
#     .execute()
# )

# cabinet_name = "Inconnu"
# if res.data and len(res.data) > 0:
#     first_row = res.data[0]
#     cabinet_data = first_row.get("cabinets", {})
#     if isinstance(cabinet_data, dict):
#         cabinet_name = cabinet_data.get("nom", "Inconnu")

# # Ensuite tu crées ton config_db avec ce cabinet_name
