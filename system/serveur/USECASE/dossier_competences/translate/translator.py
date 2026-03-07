from deep_translator import GoogleTranslator

def translate_json(data, translator):
    """Recursively translates JSON values from any language to French"""
    if isinstance(data, dict):
        return {k: translate_json(v, translator) for k, v in data.items()}
    elif isinstance(data, list):
        return [translate_json(item, translator) for item in data]
    elif isinstance(data, str) and data.strip():
        try:
            return translator.translate(data)
        except:
            return data
    return data