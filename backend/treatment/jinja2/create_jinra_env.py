from jinja2 import Environment, FileSystemLoader

def create_jinra_env(doc):
        doc.jinja_env = Environment(
                loader=FileSystemLoader("template"),
                trim_blocks=True,
                lstrip_blocks=True
            )