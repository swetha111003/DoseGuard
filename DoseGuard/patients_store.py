import json
import os
import uuid

DATA_FILE = "patients.json"

def load_patients():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_patients(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_patient(patient):
    data = load_patients()
    patient["id"] = str(uuid.uuid4())
    data.append(patient)
    save_patients(data)
