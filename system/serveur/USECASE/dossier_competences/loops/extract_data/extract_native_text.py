def extract_native_text(doc):
    return "\n".join(" ".join(s["text"] for l in b.get("lines", []) for s in l.get("spans", []))
                     for page in doc
                     for b in sorted(page.get_text("dict").get("blocks", []), key=lambda x: (x["bbox"][1]//5, x["bbox"][0])))