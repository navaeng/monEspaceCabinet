def fix_logiciels_outils(data):
    if "Logiciels_par_titre" not in data:
        return data

    for bloc in data["Logiciels_par_titre"]:
        outils = bloc.get("logiciels_outils", [])

        if isinstance(outils, list):
            bloc["logiciels_outils"] = ", ".join(outils)

        elif isinstance(outils, str):
            bloc["logiciels_outils"] = outils.strip()

    return data