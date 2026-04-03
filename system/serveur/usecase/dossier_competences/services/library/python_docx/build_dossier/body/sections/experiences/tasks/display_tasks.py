from docx.shared import Cm, RGBColor

#
# def display_tasks(doc, exp):
#     for tache in exp.get('Liste_Tâches', []):
#         p_tache = doc.add_paragraph(tache, style='List Bullet')
#         p_tache.paragraph_format.keep_together = True
#         p_tache.paragraph_format.keep_with_next = True
#         p_tache.paragraph_format.left_indent = Cm(1.25)
#         p_tache.paragraph_format.keep_with_next = True
#         for run in p_tache.runs:
#             run.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

def display_tasks(doc, exp):
        tasks = exp.get('Liste_Tâches', [])
        has_next_section = bool(exp.get("Logiciels_et_outils_utilisés_Sans_Indiquer_Le_Niveau"))

        for i, tache in enumerate(tasks):
            p_tache = doc.add_paragraph(tache, style='List Bullet')
            p_tache.paragraph_format.keep_together = True
            p_tache.paragraph_format.left_indent = Cm(1.25)

            if i < len(tasks) - 1 or has_next_section:
                p_tache.paragraph_format.keep_with_next = True

            for run in p_tache.runs:
                run.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
