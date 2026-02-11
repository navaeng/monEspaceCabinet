import threading
from collections import defaultdict

user_lock = defaultdict(threading.Lock)
