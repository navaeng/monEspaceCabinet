from docx.shared import RGBColor


def right_cells(cells, diplome):
    p_right = cells[1].paragraphs[0]
    p_right.alignment = 2
    run_date = p_right.add_run(str(diplome.get('Année', '')))
    run_date.font.color.rgb = RGBColor(0x00, 0x20, 0x60)