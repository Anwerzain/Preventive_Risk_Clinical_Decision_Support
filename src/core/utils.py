import random
from datetime import datetime

def generate_patient_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    return f"PID-{date_part}-{random_part}"
