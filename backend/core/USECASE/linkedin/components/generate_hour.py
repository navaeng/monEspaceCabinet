import random
from datetime import datetime, timedelta


def generate_hour():
    generate_hour = (datetime.now().astimezone() + timedelta(days=1)).replace(
        hour=random.randint(8, 19),
        minute=random.randint(0, 59),
    )

    return generate_hour
