from docx.shared import RGBColor, Pt


def display_logiciels_outils(doc, exp):
    p_outils = doc.add_paragraph()

    liste_outils = exp.get('Logiciels_outils', [])
    print(liste_outils)
    texte_outils = ", ".join(liste_outils) if isinstance(liste_outils, list) else str(liste_outils)

    run_label = p_outils.add_run("Logiciels et outils : ")
    run_label.bold = True

    run_liste = p_outils.add_run(texte_outils)
    run_liste.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    p_outils.paragraph_format.space_before = Pt(6)
    p_outils.paragraph_format.space_after = Pt(10)