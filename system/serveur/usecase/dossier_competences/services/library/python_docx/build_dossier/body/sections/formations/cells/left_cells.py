from docx.shared import RGBColor


def left_cells(cells, diplome):
    p = cells[0].paragraphs[0]
    p.paragraph_format.keep_with_next = True

    run_dip = p.add_run(diplome.get('Diplôme', ''))
    run_dip.bold = True
    run_dip.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    run_info = p.add_run(f"\n{diplome.get('École', '')} - {diplome.get('Lieu', '')}")
    run_info.font.color.rgb = RGBColor(0x00, 0x20, 0x60)