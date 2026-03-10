from docx.shared import Pt, Cm


def display_tasks(doc, exp):
    for tache in exp.get('Liste_Tâches', []):
        p_tache = doc.add_paragraph(tache, style='List Bullet')
        p_tache.paragraph_format.left_indent = Cm(1.25)
        p_tache.paragraph_format.keep_with_next = True