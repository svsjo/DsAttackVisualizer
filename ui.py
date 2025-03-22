import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from model import AttackData

class AttackVisualizationApp:
    """
    UI-Anwendung für die Angriffsvisualisierung.
    Die Datenhaltung erfolgt ausschließlich über das Modell (AttackData).
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Angriffsvisualisierung - Die Stämme")
        self.root.geometry("1280x720")  # Standardgröße, damit auf FHD alles sichtbar ist

        self.data = AttackData()
        self.setup_ui()
        self.load_app_data()

    def setup_ui(self):
        """Erstellt und ordnet die UI-Elemente an."""
        # Konfiguration des Root-Fensters für dynamisches Wachstum
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        mainframe = ttk.Frame(self.root)
        mainframe.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        mainframe.rowconfigure(1, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)

        # Eingabefeld für Angriffe
        ttk.Label(mainframe, text="Angriffe (Copy/Paste)").grid(row=0, column=0, columnspan=2, sticky="w")
        self.angriffe_text = scrolledtext.ScrolledText(mainframe, width=80, height=20)
        self.angriffe_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Wachtürme (eigene)
        ttk.Label(mainframe, text="Wachtürme (grün)").grid(row=2, column=0, sticky="w")
        self.wachturm_text = scrolledtext.ScrolledText(mainframe, width=40, height=10)
        self.wachturm_text.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # Sim-Wachtürme
        ttk.Label(mainframe, text="Sim-Wachtürme (blau)").grid(row=2, column=1, sticky="w")
        self.simwt_text = scrolledtext.ScrolledText(mainframe, width=40, height=10)
        self.simwt_text.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # Eigene Dörfer
        ttk.Label(mainframe, text="Eigene Dörfer (gelb)").grid(row=4, column=0, sticky="w")
        self.eigene_text = scrolledtext.ScrolledText(mainframe, width=40, height=10)
        self.eigene_text.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Feind-Dörfer
        ttk.Label(mainframe, text="Feind-Dörfer (rot)").grid(row=4, column=1, sticky="w")
        self.feind_text = scrolledtext.ScrolledText(mainframe, width=40, height=10)
        self.feind_text.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        # Stamm-Dörfer
        ttk.Label(mainframe, text="Stamm-Dörfer (blau)").grid(row=6, column=0, sticky="w")
        self.stamm_text = scrolledtext.ScrolledText(mainframe, width=40, height=10)
        self.stamm_text.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

        # Aktualisieren-Button
        update_btn = ttk.Button(mainframe, text="🔄 Aktualisieren", command=self.aktualisieren)
        update_btn.grid(row=7, column=1, pady=10)

        # Statusanzeige
        self.status_label = ttk.Label(mainframe, text="Status: ")
        self.status_label.grid(row=8, column=0, columnspan=2, sticky="w")

        # Neuer Canvas-Bereich mit Grid-Layout für Canvas und Toolbar
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")
        canvas_frame.rowconfigure(0, weight=1)  # Canvas soll den Großteil des Platzes einnehmen
        canvas_frame.rowconfigure(1, weight=0)  # Toolbar behält feste Höhe
        canvas_frame.columnconfigure(0, weight=1)

        # Erstelle einmalig die Figure und Achse
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Erstelle einen separaten Frame für die Toolbar innerhalb von canvas_frame
        toolbar_frame = ttk.Frame(canvas_frame)
        toolbar_frame.grid(row=1, column=0, sticky="ew")

        # Erstelle die Navigation-Toolbar mit toolbar_frame als Master,
        # sodass die pack()-Aufrufe nur in diesem Unterframe wirken.
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

        # Setze das Label für die Mausposition in einer weiteren Zeile
        self.pos_label = ttk.Label(canvas_frame, text="Maus Position: x=?, y=?")
        self.pos_label.grid(row=2, column=0, sticky="w", pady=(5, 0))

        self.canvas.mpl_connect('scroll_event', self.zoom)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.press = None  # Variable zur Speicherung des Panning-Zustands
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion_pan)

    def draw_chart(self):
        """Zeichnet die Karte in die bestehende Achse (self.ax)."""
        self.ax.clear()

        # Feind-Dörfer (rot)
        for dorf in self.data.feind_dorfer:
            self.ax.plot(*dorf, color='orange', marker='o', markersize=1.5, zorder=0)

        # Angriffe
        for ziel, start, _ in self.data.alle_angriffe:
            self.ax.plot(*start, color='red', marker='o', markersize=1.5, zorder=2)
            self.ax.plot(*ziel, color='orange', marker='o', markersize=1.8, zorder=2)
            self.ax.annotate("", xy=ziel, xytext=start,
                             arrowprops=dict(arrowstyle="->", color='grey', linewidth=0.1), zorder=1)

        # Eigene Dörfer (gelb)
        for dorf in self.data.eigene_dorfer:
            self.ax.plot(*dorf, color='yellow', marker='o', markersize=1.5, zorder=3)

        # Stammdörfer (blau)
        for dorf in self.data.stamm_dorfer:
            self.ax.plot(*dorf, color='blue', marker='o', markersize=1.5, zorder=3)

        # Wachturm-Kreise (gelb/schwarz)
        for dorf in self.data.wachturmdorfer:
            kreis = plt.Circle(dorf, 15, color='black', fill=False, linewidth=1.2, linestyle='--', zorder=4)
            self.ax.add_patch(kreis)
            self.ax.plot(*dorf, color='yellow', marker='o', markersize=2, zorder=5)

        # SimWT-Kreise (grün)
        for dorf in self.data.simwt_dorfer:
            kreis = plt.Circle(dorf, 15, color='green', fill=False, linewidth=1.5, linestyle='--', zorder=4)
            self.ax.add_patch(kreis)
            self.ax.plot(*dorf, color='green', marker='o', markersize=2, zorder=5)

        self.ax.set_title("Angriffsübersicht")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()

    def update_canvas(self):
        """Aktualisiert den Matplotlib-Canvas, indem die Karte neu gezeichnet wird."""
        self.draw_chart()
        self.canvas.draw_idle()

    def zoom(self, event):
        """Reagiert auf das Mausrad zum Zoomen in der Karte."""
        ax = self.ax  # Verwende die persistente Achse
        base_scale = 1.2
        xdata = event.xdata
        ydata = event.ydata
        if xdata is None or ydata is None:
            return
        scale_factor = 1 / base_scale if event.button == 'up' else base_scale if event.button == 'down' else 1
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        self.canvas.draw_idle()

    def on_press(self, event):
        """Speichert die Startposition und die aktuellen Achsengrenzen beim Mausklick."""
        if event.inaxes:
            self.press = (event.xdata, event.ydata, self.ax.get_xlim(), self.ax.get_ylim())

    def on_motion_pan(self, event):
        """
        Berechnet während des Ziehens die Verschiebung und aktualisiert die Achsengrenzen,
        sofern die linke Maustaste gedrückt ist.
        """
        if self.press is None or event.inaxes is None:
            return
        xpress, ypress, xlim, ylim = self.press
        dx = xpress - event.xdata
        dy = ypress - event.ydata
        self.ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
        self.ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
        self.canvas.draw_idle()

    def on_release(self, event):
        """Setzt den Panning-Zustand zurück, sobald die Maustaste losgelassen wird."""
        self.press = None

    def on_mouse_move(self, event):
        """Aktualisiert die Anzeige der Mausposition basierend auf den Ereignisdaten."""
        if event.inaxes:
            self.pos_label.config(text=f"Maus Position: x={event.xdata:.1f}, y={event.ydata:.1f}")
        else:
            self.pos_label.config(text="Maus Position: außerhalb der Karte")

    def update_status(self):
        """Aktualisiert die Statusanzeige anhand der aktuellen Modell-Daten."""
        status_text = (f"Status: {len(self.data.alle_angriffe)} Angriffe, "
                       f"{len(self.data.wachturmdorfer)} Wachturm, {len(self.data.simwt_dorfer)} SimWT, "
                       f"{len(self.data.eigene_dorfer)} Eigene, {len(self.data.feind_dorfer)} Feind, "
                       f"{len(self.data.stamm_dorfer)} Stamm")
        self.status_label.config(text=status_text)

    def aktualisieren(self):
        """
        Liest die Texteingaben, aktualisiert das Modell, speichert den Zustand und
        aktualisiert anschließend die Anzeige (Karte und Status).
        """
        angriffe = self.angriffe_text.get("1.0", tk.END)
        wachturm = self.wachturm_text.get("1.0", tk.END)
        simwt = self.simwt_text.get("1.0", tk.END)
        eigene = self.eigene_text.get("1.0", tk.END)
        feind = self.feind_text.get("1.0", tk.END)
        stamm = self.stamm_text.get("1.0", tk.END)

        self.data.update_from_text(angriffe, wachturm, simwt, eigene, feind, stamm)
        self.data.save()
        self.update_canvas()
        self.update_status()

    def load_app_data(self):
        """Lädt den gespeicherten Zustand und füllt die UI-Felder entsprechend."""
        self.data.load()
        texts = self.data.texts
        self.angriffe_text.insert("1.0", texts.get("angriffe", ""))
        self.wachturm_text.insert("1.0", texts.get("wachturm", ""))
        self.simwt_text.insert("1.0", texts.get("simwt", ""))
        self.eigene_text.insert("1.0", texts.get("eigene", ""))
        self.feind_text.insert("1.0", texts.get("feind", ""))
        self.stamm_text.insert("1.0", texts.get("stamm", ""))
        self.update_canvas()
        self.update_status()
