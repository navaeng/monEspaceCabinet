from data.extract_data.extract_diplomes import extract_diplomes_from_cv
from data.extract_data.extract_experiences import extract_experiences_from_cv
from data.extract_data.extract_infos import extract_infos_from_cv
from data.extract_data.extract_skills_tools import extract_skills_tools_from_cv


def extract_and_call_prompt(selected_file, file_label, self, offer_file=None):
    file_label.setText("Lancement...")

    data_skills_tools = extract_skills_tools_from_cv(selected_file, self)
    file_label.setText("Extractions des compétences...")

    data_infos = extract_infos_from_cv(selected_file)
    file_label.setText("Extractions des informations personnelles...")

    data_diplomes = extract_diplomes_from_cv(selected_file)
    file_label.setText("Extractions des diplômes...")

    data_experiences = extract_experiences_from_cv(selected_file)
    file_label.setText("Extraction terminée")

    return (
        data_skills_tools,
        data_infos,
        data_diplomes,
        data_experiences,
    )
