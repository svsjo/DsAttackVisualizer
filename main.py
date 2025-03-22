import tkinter as tk
from ui import AttackVisualizationApp

def main():
    root = tk.Tk()

    root.attributes("-fullscreen", True)  # Startet die Anwendung im Vollbildmodus

    # Optionale Bindung, um den Vollbildmodus wieder zu verlassen (z. B. bei Escape)
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

    # Stelle sicher, dass beim Schließen das Programm beendet wird:
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    app = AttackVisualizationApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
