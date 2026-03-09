from docx.opc.oxml import qn
from docx.oxml import OxmlElement

def shadow_cells(table):

    tbl = table._tbl
    tblPr = tbl.get_or_add_tblPr()
    tblBorders = OxmlElement("w:tblBorders")

    for tag in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        border = OxmlElement(f'w:{tag}')
        border.set(qn('w:val'), 'nil')
        tblBorders.append(border)

    tblPr.append(tblBorders)