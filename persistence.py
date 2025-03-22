import json
import os

SAVE_FILE = "angriffsvisualisierung_data.json"

def save_state(state: dict, save_file: str = SAVE_FILE):
    """Speichert den Zustand als JSON-Datei."""
    try:
        with open(save_file, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Fehler beim Speichern des Zustands: {e}")

def load_state(save_file: str = SAVE_FILE) -> dict:
    """Lädt den Zustand aus der JSON-Datei, sofern vorhanden."""
    if os.path.exists(save_file):
        try:
            with open(save_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden des Zustands: {e}")
    return {}
