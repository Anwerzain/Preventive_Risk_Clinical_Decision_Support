def authenticate(username, password):
    DOCTORS = {
        "doctor1": "pass123",
        "doctor2": "admin123"
    }
    return username in DOCTORS and DOCTORS[username] == password
