from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.shared import Cm
from docx.oxml.ns import nsdecls

def header_left(logo_path, p):
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    run_logo = p.add_run()
    run_logo.add_picture(logo_path, width=Cm(2.83), height=Cm(2.87))

    inline = run_logo._element.xpath('.//wp:inline')[0]
    anchor_xml = inline.xml.replace('wp:inline', 'wp:anchor').replace(
        'distT="0" distB="0" distL="0" distR="0"',
        'distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="251658240" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1"'
    ).replace(
        '</wp:docPr>',
        '</wp:docPr><wp:positionH relativeFrom="page"><wp:posOffset>360000</wp:posOffset></wp:positionH><wp:positionV relativeFrom="page"><wp:posOffset>360000</wp:posOffset></wp:positionV>'
    )
    new_anchor = parse_xml(anchor_xml)
    inline.getparent().replace(inline, new_anchor)