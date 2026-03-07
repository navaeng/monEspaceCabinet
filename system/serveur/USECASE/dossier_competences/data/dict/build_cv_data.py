def build_cv_data(data_skills_tools, data_experiences, data_infos, data_diplomes, all_data):

    cv_data = {
        "cv_texte_propre": all_data,
        **(data_skills_tools or {}),
        **(data_infos or {}),
        **(data_diplomes or {}),
        **(data_experiences or {}),
    }

    return cv_data