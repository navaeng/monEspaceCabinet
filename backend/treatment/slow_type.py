import random
import time


def slow_type(element, text):

    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))
