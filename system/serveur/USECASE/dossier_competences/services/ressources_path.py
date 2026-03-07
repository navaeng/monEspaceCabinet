import os
import sys


def ressources_path(relative_path):
    if getattr(sys, "frozen", False):
        if sys.platform.system() == "Darwin":
            base_path = os.path.join((sys.executable), "../../../../../..", "Resources")
        else:
            base_path = sys._MEIPASS

    else:
        base_path = os.path.abspath("../../../../..")
    return os.path.join(base_path, relative_path)