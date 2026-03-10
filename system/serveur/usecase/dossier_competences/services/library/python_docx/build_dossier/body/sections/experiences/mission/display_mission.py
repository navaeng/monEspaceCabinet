from docx.shared import Pt, RGBColor


def display_mission(doc, exp):
    p_mission = doc.add_paragraph()

    run_label = p_mission.add_run("MISSION : ")
    run_label.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
    run_label.bold = True
    run_label.underline = True

    run_desc = p_mission.add_run(str(exp.get('Résumé_concis_tâches_à_définir', '')))
    run_desc.font.color.rgb = RGBColor(0, 0, 0)

    p_mission.paragraph_format.space_before = Pt(10)
    p_mission.paragraph_format.space_after = Pt(10)
    p_mission.paragraph_format.keep_with_next = True