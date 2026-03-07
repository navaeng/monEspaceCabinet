import re
def replace_level_language(obj):
    level_map = {
        "A1": "Débutant",
        "A2": "Élémentaire",
        "B1": "Intermédiaire",
        "B2": "Intermédiaire avancé",
        "C2": "Maîtrise",
        "C1": "Avancé"
    }

    if isinstance(obj, str):
        def replace(match):
            level = match.group(1)
            return f"({level_map.get(level, level)})"
        
        return re.sub(r'\(([ABC][12])\)', replace, obj)
    elif isinstance(obj, dict):
            return {k: replace_level_language(v) for k, v in obj.items()}
    elif isinstance(obj, list):
            return [replace_level_language(item) for item in obj]
    return obj