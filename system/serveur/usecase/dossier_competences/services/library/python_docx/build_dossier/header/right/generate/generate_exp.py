def generate_exp(data):
    exp_val = str(data.get('Expérience_Totale_Années', ''))
    if exp_val and "exp" not in exp_val.lower():
        exp_val += " ans d'expérience"

    return exp_val