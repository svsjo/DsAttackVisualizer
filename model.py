from utils import parse_angriffe, parse_coords
from persistence import save_state, load_state

class AttackData:
    """
    Modell zur Verwaltung der Angriffs-Daten.
    Hält die aktuellen Daten und Texteingaben, bietet Methoden zum Aktualisieren, Speichern und Laden.
    """
    def __init__(self):
        self.alle_angriffe = set()    # ((ziel_x, ziel_y), (start_x, start_y), uhrzeit)
        self.wachturmdorfer = set()
        self.simwt_dorfer = set()
        self.eigene_dorfer = set()
        self.feind_dorfer = set()
        self.stamm_dorfer = set()
        self.texts = {
            "angriffe": "",
            "wachturm": "",
            "simwt": "",
            "eigene": "",
            "feind": "",
            "stamm": ""
        }

    def update_from_text(self, angriffe_text: str, wachturm_text: str, simwt_text: str,
                         eigene_text: str, feind_text: str, stamm_text: str):
        """
        Aktualisiert die Daten und Texteingaben basierend auf den übergebenen Texten.
        """
        self.texts["angriffe"] = angriffe_text
        self.texts["wachturm"] = wachturm_text
        self.texts["simwt"] = simwt_text
        self.texts["eigene"] = eigene_text
        self.texts["feind"] = feind_text
        self.texts["stamm"] = stamm_text

        self.alle_angriffe = parse_angriffe(angriffe_text)
        self.wachturmdorfer = parse_coords(wachturm_text)
        self.simwt_dorfer = parse_coords(simwt_text)
        self.eigene_dorfer = parse_coords(eigene_text)
        self.feind_dorfer = parse_coords(feind_text)
        self.stamm_dorfer = parse_coords(stamm_text)

    def to_dict(self):
        """Konvertiert den aktuellen Zustand in ein Dictionary zur Persistenz."""
        return {
            "angriffe": [[list(a[0]), list(a[1]), a[2]] for a in self.alle_angriffe],
            "wachturm": list(self.wachturmdorfer),
            "simwt": list(self.simwt_dorfer),
            "eigene": list(self.eigene_dorfer),
            "feind": list(self.feind_dorfer),
            "stamm": list(self.stamm_dorfer),
            "texte": self.texts
        }

    def from_dict(self, data: dict):
        """Lädt den Zustand aus dem übergebenen Dictionary."""
        self.alle_angriffe = set((tuple(a[0]), tuple(a[1]), a[2]) for a in data.get("angriffe", []))
        self.wachturmdorfer = set(tuple(a) for a in data.get("wachturm", []))
        self.simwt_dorfer = set(tuple(a) for a in data.get("simwt", []))
        self.eigene_dorfer = set(tuple(a) for a in data.get("eigene", []))
        self.feind_dorfer = set(tuple(a) for a in data.get("feind", []))
        self.stamm_dorfer = set(tuple(a) for a in data.get("stamm", []))
        self.texts = data.get("texte", self.texts)

    def save(self):
        """Speichert den aktuellen Zustand mithilfe des persistence-Moduls."""
        state = self.to_dict()
        save_state(state)

    def load(self):
        """Lädt den Zustand mithilfe des persistence-Moduls."""
        data = load_state()
        if data:
            self.from_dict(data)