import re

def parse_angriffe(text: str) -> set:
    """
    Parst Angriffsdaten aus dem übergebenen Text.
    Gibt eine Menge von Tupeln ((ziel_x, ziel_y), (start_x, start_y), uhrzeit) zurück.
    """
    pattern = re.compile(
        r'\((\d{3})\|(\d{3})\).*?\((\d{3})\|(\d{3})\).*?(\d{1,2}[:\.]\d{2}[:\.]\d{2})'
    )
    result = set()
    for line in text.strip().split("\n"):
        match = pattern.search(line)
        if match:
            try:
                ziel = (int(match.group(1)), int(match.group(2)))
                start = (int(match.group(3)), int(match.group(4)))
                uhrzeit = match.group(5).replace(".", ":")
                result.add((ziel, start, uhrzeit))
            except Exception as e:
                print(f"Fehler beim Parsen der Zeile: {line} - {e}")
    return result

def parse_coords(text: str) -> set:
    """
    Parst Koordinaten aus dem übergebenen Text.
    Gibt eine Menge von Tupeln (x, y) zurück.
    """
    pattern = re.compile(r'(\d{3})\|(\d{3})')
    return set((int(x), int(y)) for x, y in pattern.findall(text))
