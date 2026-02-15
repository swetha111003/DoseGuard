import json
import os

DATA_FILE = "patient.json"

def save_patient(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_patient():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r") as f:
        return json.load(f)
