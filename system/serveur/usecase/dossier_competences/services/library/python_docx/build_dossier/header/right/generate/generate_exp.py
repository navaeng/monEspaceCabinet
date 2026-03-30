def generate_exp(data):
    try:
        val = float(str(data.get('Expérience_Totale_Années', '')).split('an')[0].strip())
        ans = int(val)
        mois = round((val - ans) * 12)

        print(val, ans)

        parts = []
        if ans > 0: parts.append(f"{ans} an{'s' if ans > 1 else ''}")
        if mois > 0: parts.append(f"{mois} mois")

        return " et ".join(parts) + " d'expérience" if parts else "Moins d'un an d'expérience"

    except:
        return f"{data.get('Expérience_Totale_Années', '')} d'expérience"
