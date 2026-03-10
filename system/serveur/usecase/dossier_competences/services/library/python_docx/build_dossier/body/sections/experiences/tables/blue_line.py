from docx.opc.oxml import qn, parse_xml
from docx.oxml.ns import nsdecls

def blue_line(table):
    for cell in table.rows[0].cells:
        tcPr = cell._element.get_or_add_tcPr()
        border_xml = f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:color="1B4A8A"/></w:tcBorders>'
        tcPr.append(parse_xml(border_xml))

