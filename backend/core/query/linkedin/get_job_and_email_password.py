def get_job_and_email_password(config_db, job):
        config_db = {
                                        **job,
                                        **(
                                            config_db
                                            if isinstance(config_db, dict)
                                            else {}
                                        ),
                                    }