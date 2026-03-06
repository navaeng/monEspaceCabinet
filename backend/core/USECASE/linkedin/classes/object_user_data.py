def object_user_data(data, current_user_id, body):
    user_data = {
        "id": data.get("id"),
        "user_id": current_user_id,
        "linkedin_email": data.get("linkedin_email"),
        "linkedin_password": data.get("linkedin_password"),
        "job_title": body.intitule,
        "full_name": data.get("full_name"),
        "telephone": data.get("telephone"),
        "cabinet_name": data.get("cabinet_name"),
    }
    print(user_data)
    return user_data
