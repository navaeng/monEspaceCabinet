import re 

def replace_ampersand(obj):
    if isinstance(obj, str):
        return re.sub(r'@amp;|(?<!&)&(?![a-zA-Z]+;)', 'et', obj)
    elif isinstance(obj, dict):
        return {k: replace_ampersand(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_ampersand(item) for item in obj]
    return obj