import threading
import traceback

from data.extract_data.extract_offer import extract_offer
from layout.data.result_analyse_offer import result_analyse_offer
from treatment.buttons.enabled_false_all_buttons import enabled_false_all_buttons


def analyser_cv_offre(self):
    if not hasattr(self, "_signal_connected"):
        self.update_ui.connect(lambda data: result_analyse_offer(data, self))
        self._signal_connected = True

    def worker():
        try:
            print("analyse en cours...")
            self.status_signal.emit("Analyse en cours...")
            enabled_false_all_buttons(self)

            offer_file = self.selected_offer
            cvs = self.selected_cv

            data_offer = extract_offer(offer_file, cvs)

            if not data_offer:
                raise ValueError("Les données n'ont pas pu être extraites.")
            print("Data reçue, affichage dans le layout...")

            self.update_ui.emit(data_offer)

        except Exception as e:
            error_msg = f"Erreur: {str(e)}\n{traceback.format_exc()}"
            self.file_label.setText(error_msg[:600])
            self.upload_btn.setEnabled(True)
            print(error_msg)

            self.file_label.setText(error_msg)

    enabled_false_all_buttons(self)

    threading.Thread(
        target=worker,
        daemon=True,
    ).start()
