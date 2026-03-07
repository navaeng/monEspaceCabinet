from USECASE.dossier_competences.data.extract_data_from_cv.extract_cv import extract_and_read_cv
from USECASE.dossier_competences.data.extract_data_from_cv.analyse_diplomes_with_model import extract_diplomes_from_cv
from USECASE.dossier_competences.data.extract_data_from_cv.analyse_experiences_with_model import extract_experiences_from_cv
from USECASE.dossier_competences.data.extract_data_from_cv.analyse_infos_with_model import extract_infos_from_cv
from USECASE.dossier_competences.data.extract_data_from_cv.analyse_skills_tools_with_model import extract_skills_tools_from_cv


def extract_and_call_prompt(
    cv_file_path
):
    selected_file = cv_file_path

    clean_text = extract_and_read_cv(selected_file)

    data_skills_tools = extract_skills_tools_from_cv(clean_text)

    data_infos = extract_infos_from_cv(clean_text)

    data_diplomes = extract_diplomes_from_cv(clean_text)

    data_experiences = extract_experiences_from_cv(clean_text)

    return clean_text, data_skills_tools, data_infos, data_diplomes, data_experiences
