from data.extract_data.extract_and_read_cv import extract_and_read_cv
from data.extract_data.extract_diplomes import extract_diplomes_from_cv
from data.extract_data.extract_experiences import extract_experiences_from_cv
from data.extract_data.extract_infos import extract_infos_from_cv
from data.extract_data.extract_skills_tools import extract_skills_tools_from_cv


def extract_and_call_prompt_api(
    cv_file_path, add_skills, english_cv=False, progress_callback=None
):
    print(f"DEBUG BACKEND: add_skills vaut {add_skills} (type: {type(add_skills)})")
    selected_file = cv_file_path

    def log(msg):
        if progress_callback:
            progress_callback(msg)
        print(f"📊 {msg}")

    class FakeSelf:
        def __init__(self):
            self.add_skills_yes = FakeCheckbox(add_skills)
            self.add_skills_no = FakeCheckbox(not add_skills)
            self.english_cv = FakeCheckbox(english_cv)

    class FakeCheckbox:
        def __init__(self, checked):
            self._checked = checked

        def isChecked(self):
            return self._checked

    fake_self = FakeSelf()

    log("Lancement...")

    clean_text = extract_and_read_cv(selected_file)

    log("Extraction des skills...")
    data_skills_tools = extract_skills_tools_from_cv(clean_text, fake_self)

    log("Extraction des informations personnelles...")
    data_infos = extract_infos_from_cv(clean_text)

    log("Extraction des diplômes...")
    data_diplomes = extract_diplomes_from_cv(clean_text)

    log("Extraction des expériences...")
    data_experiences = extract_experiences_from_cv(clean_text)

    log("Extraction terminée")

    return clean_text, data_skills_tools, data_infos, data_diplomes, data_experiences
