from core.query.rpc_query import rpc_query


def get_user_informations(user_data):

    rpc_res = rpc_query(user_data)

    if rpc_res.data and len(rpc_res.data) > 0:
        decrypted = rpc_res.data[0]
        user_data["linkedin_email"] = decrypted.get("linkedin_email")
        user_data["linkedin_password"] = decrypted.get("linkedin_password")
        user_data["full_name"] = decrypted.get("full_name")
        user_data["telephone"] = decrypted.get("telephone")

    print(f"linkedin_email: {user_data['linkedin_email']}")
    return user_data