"""
UI Manager
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import tkinter as tk

class UIManager:
    """
    UI Manager
    """
    def __init__(self, vill) -> None:
        self._running = False

        self._root = tk.Tk()
        self._root.title("Village Skylines")
        self._root.geometry("800x600")
        self._root.protocol("WM_DELETE_WINDOW", self.quit)

        self._x = 0

        self._label = tk.Label(self._root, text=str(self._x))
        self._label.pack()

        self._vill = vill

    def run(self) -> None:
        """
        main ui loop
        """
        self._running = True
        while self._running:
            self._root.update()
            self._x = self._vill._money
            self._label.config(text = str(self._x))
        self._root.destroy()

    def quit(self) -> None:
        """
        quit
        """
        self._running = False
        print("quitting")
