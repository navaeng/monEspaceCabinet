from treatment.translate.translator import translate_json
from deep_translator import GoogleTranslator

def translate(data, self):
        translator = GoogleTranslator(source='auto', target='fr')
        self.file_label.setText("Traduction en cours...")
        data = translate_json(data, translator)
        self.file_label.setText("Traduction terminée")
        return data