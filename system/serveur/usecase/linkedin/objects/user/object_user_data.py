def object_user_data(body, current_user_id):
    data = body.model_dump()
    user_data = {
        "id": data.get("id"),
        "cabinet_id": data.get("cabinet_id"),
        "user_id": current_user_id,
        "linkedin_email": data.get("linkedin_email"),
        "linkedin_password": data.get("linkedin_password"),
        "job_title": body.intitule,
        "full_name": data.get("full_name"),
        "telephone": data.get("telephone"),
        "cabinet_name": data.get("cabinet_name"),
        "origin_mode": data.get("mode"),
    }
    print(user_data)
    return user_data