from docx.shared import Pt, RGBColor


def display_poste(doc, exp):
    p_poste = doc.add_paragraph()
    run_poste = p_poste.add_run(str(exp.get('Poste_Occupé', '')).upper())
    run_poste.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    run_poste.bold = True
    run_poste.underline = True

    p_poste.paragraph_format.space_before = Pt(10)
    p_poste.paragraph_format.space_after = Pt(10)

    p_poste.paragraph_format.keep_with_next = True
