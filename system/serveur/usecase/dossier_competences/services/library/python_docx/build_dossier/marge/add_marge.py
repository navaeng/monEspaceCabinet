from docx.shared import Cm

def add_marge(doc):

    for section in doc.sections:
        section.top_margin = Cm(3)