from datetime import time
from random import random

from core.query.cabinets.get_cabinets_name import get_cabinets_name


def get_cabinet_name(infos_profil):

    cabinet_name = get_cabinets_name()
    if cabinet_name:
        exclusions = [cabinet_name, cabinet_name.replace(" ", "")]
        print(f"Exclusions: {exclusions}")

    return cabinet_name, exclusions