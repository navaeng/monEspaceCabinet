from data.database import supabase_client
from usecase.linkedin.query.functions.rpc.rpc_query import rpc_query


# def object_user_data(body, current_user_id):
#     data = body.model_dump()
#     user_data = {
#         "id": data.get("id"),
#         "cabinet_id": data.get("cabinet_id"),
#         "user_id": current_user_id,
#         "linkedin_email": data.get("linkedin_email"),
#         "linkedin_password": data.get("linkedin_password"),
#         "job_title": body.intitule,
#         "full_name": data.get("full_name"),
#         "telephone": data.get("telephone"),
#         "cabinet_name": data.get("cabinet_name"),
#         "origin_mode": data.get("mode"),
#     }
#     print(user_data)
#     return user_data

def get_user_data(body, current_user_id):
    result = supabase_client().table("profiles") \
        .select("*") \
        .eq("id", current_user_id) \
        .single() \
        .execute()
    profile = result.data

    rpc_res = rpc_query({
        "job_title": body.intitule
    })

    print(f"DEBUG credentials: {rpc_res.data}")
    creditendials = rpc_res.data[0] if rpc_res.data else {}

    user_data = {
        "id": profile.get("id"),
        "user_id": current_user_id,
        "linkedin_email": profile.get("linkedin_email"),
        "linkedin_password": creditendials.get("pgp_sym_decrypt"),
        "job_title": body.intitule,
        "full_name": profile.get("full_name"),
        "telephone": profile.get("telephone"),
        "cabinet_name": profile.get("cabinet_name"),
        "origin_mode": body.mode,
    }
    return user_data