from docx.oxml.ns import qn
from docx.oxml import parse_xml


def header_section(doc, texte):
    p = doc.add_paragraph()
    p.clear()

    drawing_xml = (
        '<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
        '<w:drawing>'
        '<wp:inline>'
        '<wp:extent cx="6494400" cy="309600"/>'
        '<wp:docPr id="1" name="header"/>'
        '<a:graphic>'
        '<a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
        '<wps:wsp>'
        '<wps:spPr>'
        '<a:xfrm><a:off x="0" y="0"/><a:ext cx="6494400" cy="309600"/></a:xfrm>'
        '<a:prstGeom prst="roundRect">'
        '<a:avLst><a:gd name="adj" fmla="val 20000"/></a:avLst>'
        '</a:prstGeom>'
        '<a:gradFill>'
        '<a:gsLst>'
        '<a:gs pos="0"><a:srgbClr val="02466D"/></a:gs>'
        '<a:gs pos="100000"><a:srgbClr val="4472C4"/></a:gs>'
        '</a:gsLst>'
        '<a:lin ang="5400000" scaled="0"/>'
        '</a:gradFill>'
        '<a:ln><a:noFill/></a:ln>'
        '</wps:spPr>'
        '<wps:txbx>'
        '<w:txbxContent>'
        '<w:p>'
        '<w:pPr><w:jc w:val="center"/></w:pPr>'
        '<w:r>'
        '<w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="24"/></w:rPr>'
        f'<w:t>{texte}</w:t>'
        '</w:r>'
        '</w:p>'
        '</w:txbxContent>'
        '</wps:txbx>'
        '<wps:bodyPr/>'
        '</wps:wsp>'
        '</a:graphicData>'
        '</a:graphic>'
        '</wp:inline>'
        '</w:drawing>'
        '</w:r>'
    )
    p._element.append(parse_xml(drawing_xml))