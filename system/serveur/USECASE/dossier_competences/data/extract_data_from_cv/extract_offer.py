import html
import json

from json import extract_json

from services.read_cv import read_cv
from system.services.api_externes.groq import call_groq
from services import prompt_offre


def extract_offer(offer_file, cvs):
    print("Début de l'extracttion des fichiers")
    doc_text = read_cv(offer_file)
    doc_size = len(doc_text.split())
    print("documents lu, longueur :", doc_size)

    cvs_texts = [read_cv(cv) for cv in cvs]
    prompt = prompt_offre(doc_text, cvs_texts)
    print("⚡ travail en cours des offres…")
    output = call_groq(prompt)

    data_offer = {}
    if output:
        json_text = extract_json(output).strip()
        json_text = (
            json_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

        try:
            json_text = f"[{json_text}]"
            data_offer = json.loads(json_text)
            data_offer = {f"candidat{i + 1}": c for i, c in enumerate(data_offer)}
            data_offer["classement"] = [
                f"candidat{i + 1}" for i in range(len(data_offer))
            ]

            data_offer = {
                k: html.escape(v) if isinstance(v, str) else v
                for k, v in data_offer.items()
            }
        except json.JSONDecodeError as e:
            print(f"Erreur JSON : {e}")
            print("JSON brut (repr) :", repr(json_text))
            data_offer = {}

        return data_offer
