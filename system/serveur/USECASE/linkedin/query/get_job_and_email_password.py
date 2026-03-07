def get_job_and_email_password(user_data, job):
        user_data = {
                                        **job,
                                        **(
                                            user_data
                                            if isinstance(user_data, dict)
                                            else {}
                                        ),
                                    }
        return user_data