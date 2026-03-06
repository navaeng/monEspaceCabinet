def get_user_informations(job, decrypted_data):
        if isinstance(decrypted_data, dict):
            print("DEBUG - Settings linkedin successfully")
            job["linkedin_email"] = decrypted_data.get("linkedin_email")
            job["linkedin_password"] = decrypted_data.get(
                "linkedin_password"
            )
            job["full_name"] = decrypted_data.get("full_name")
            job["telephone"] = decrypted_data.get("telephone")

            print(f"linkedin_email: {job['linkedin_email']}")
            print(f"linkedin_password: {job['linkedin_password']}")
            print(f"full_name: {job['full_name']}")
            print(f"telephone: {job['telephone']}")
        else:
            print("DEBUG - Invalid settings format")