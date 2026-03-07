from docx import Document

def render_document(data, output_path):
    doc = Document()
    doc.save(output_path)