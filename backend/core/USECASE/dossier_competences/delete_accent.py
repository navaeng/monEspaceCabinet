import unicodedata


def delete_accent(s):  # on evite d'avoir des acccents
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )
