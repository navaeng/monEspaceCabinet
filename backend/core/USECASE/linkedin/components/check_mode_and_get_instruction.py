from data.prompt.prospection.prompt_message_prospection import prompt_message_prospection
from data.prompt.prospection.prompt_message_sourcing import prompt_message_sourcing


def check_mode_and_get_instruction(origin_mode,     driver,
    job_title,
    details,
    telephone,
    full_name,
    candidatrecherche):

    previous_message = []

    if origin_mode == "prospection":
        instruction = prompt_message_prospection(
            job_title, details, telephone, full_name, previous_message
        )
    elif origin_mode == "sourcing":
        instruction = prompt_message_sourcing(
            job_title, details, telephone, full_name, candidatrecherche, previous_message
        )

    return instruction