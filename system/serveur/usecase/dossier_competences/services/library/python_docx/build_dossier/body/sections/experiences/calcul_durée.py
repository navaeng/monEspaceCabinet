import datetime


def calcul_durée(exp):
    periode = exp.get('Dates_Période', '')
    if not periode: return ""

    try:
        print('début de calcul de la durée')
        dates = [d.strip() for d in periode.split('-')]
        start = datetime.strptime(dates[0], "%m/%Y")
        end = datetime.now() if any(word in dates[1].lower() for word in ["présent", "cours"]) else datetime.strptime(dates[1], "%m/%Y")

        diff_mois = (end.year - start.year) * 12 + (end.month - start.month)
        return f"\n({diff_mois // 12} an(s) {diff_mois % 12} mois)" if diff_mois >= 12 else f"\n({diff_mois} mois)"
    except Exception:
        return ""