import datetime

from dateutil.relativedelta import relativedelta


def calcul_durée_exp(exp):
    dates = exp.get('Dates_Période', '')
    print(f"--- Analyse : {dates}")
    if '/' in dates:
        try:
            parts = [d.strip() for d in dates.split('/')]
            debut = datetime.strptime(parts[0], "%m-%Y")
            fin = datetime.now() if any(
                word in parts[1].lower() for word in ["aujourd", "en cours"]) else datetime.strptime(parts[1], "%m-%Y")

            diff = relativedelta(fin, debut)
            res = []
            if diff.years > 0: res.append(f"{diff.years} an{'s' if diff.years > 1 else ''}")
            if diff.months > 0: res.append(f"{diff.months} mois")

            exp['Durée_Mission'] = " et ".join(res) if res else "Moins d'un mois"
            print(f"Résultat : {exp['Durée_Mission']}")
        except Exception as e:
            print(f"Erreur format date : {e}")
            exp['Durée_Mission'] = ""