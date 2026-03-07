def for_job_in_data(data):
                for job in data:
                    uid = job.get("user_id")
                    job_id = job.get("id")
                    title = str(job.get("job_title") or "")
                    details = str(job.get("details") or "")
                    mode = str(job.get("mode") or "")
                    candidatrecherche = str(job.get("candidatrecherche") or "")
                    post = str(job.get("post") or "")
                    telephone = str(job.get("telephone") or "")
                    full_name = str(job.get("full_name") or "")
                    cabinet_name = str(job.get("cabinet_name") or "")

