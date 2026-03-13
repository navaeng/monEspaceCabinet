from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor

def cellule_haut(tab):
            p1 = tab.cell(0, 0).paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p1.add_run()

            rPr = r._element.get_or_add_rPr()
            rPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>'))
            r.font.color.rgb = RGBColor(255, 255, 255)
            r._element.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>'))
            r._element.append(parse_xml(f'<w:instrText {nsdecls("w")}>PAGE</w:instrText>'))
            r._element.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>'))
