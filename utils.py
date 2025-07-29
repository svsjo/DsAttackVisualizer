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

def format_angriffe(angriffe: set) -> str:
    return "\n".join(
        f"({ziel[0]}|{ziel[1]}) -> ({start[0]}|{start[1]}) {uhrzeit}"
        for ziel, start, uhrzeit in sorted(angriffe)
    )

def format_coords(coords: set) -> str:
    return "\n".join(f"{x}|{y}" for x, y in sorted(coords))

def line_intersects_circle(start, end, center, radius):
    """
    Prüft, ob die Linie von start → end einen Kreis mit gegebenem center und radius schneidet.
    """
    from math import sqrt

    (x1, y1), (x2, y2) = start, end
    (cx, cy) = center

    # Vorprüfung: Bounding-Box der Linie und Kreis
    min_x = min(x1, x2) - radius
    max_x = max(x1, x2) + radius
    min_y = min(y1, y2) - radius
    max_y = max(y1, y2) + radius

    if not (min_x <= cx <= max_x and min_y <= cy <= max_y):
        return False  # Wachturm zu weit weg – kein Schnitt möglich

    # Vektor von Linie
    dx = x2 - x1
    dy = y2 - y1

    # Vektor von Linie zum Kreiszentrum
    fx = x1 - cx
    fy = y1 - cy

    a = dx*dx + dy*dy
    b = 2 * (fx*dx + fy*dy)
    c = fx*fx + fy*fy - radius*radius

    # Quadratische Gleichung lösen
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return False  # Kein Schnittpunkt

    discriminant = sqrt(discriminant)
    t1 = (-b - discriminant) / (2*a)
    t2 = (-b + discriminant) / (2*a)

    # Prüfe, ob ein Schnittpunkt auf dem Liniensegment liegt
    return 0 <= t1 <= 1 or 0 <= t2 <= 1