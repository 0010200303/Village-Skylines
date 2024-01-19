"""
Tkinter Frames
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from managers.states import State

# includes only needed for typing
if TYPE_CHECKING:
    from managers.ui_manager import UIManager
    from village import Village

class DFrame(ttk.Frame):
    """
    Frame that can be disable and enabled
    """
    style = None

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        if self.style is None:
            self.style = ttk.Style()
            self.style.configure("MainFrame.TFrame",
                                 background="pink")
            self.style.configure("Title.TLabel",
                                 foreground="Purple",
                                 background="pink",
                                 font=("Comic Sans ms", 72))
            self.style.configure("Start.TButton",
                                 foreground="green",
                                 font=("Comic Sans MS", 16),
                                 borderwidth=8,
                                 relief=tk.RAISED)
            self.style.configure("Quit.TButton",
                                 foreground="red",
                                 font=("Comic Sans MS", 16),
                                 borderwidth=8,
                                 relief=tk.RAISED)

    def _change_state(self, state: str) -> None:
        """
        Changes state of all widgets
        """
        for child in self.winfo_children():
            child.configure(state=state)

    def enable(self) -> None:
        """
        Enable frame
        """
        self._change_state("normal")

    def disable(self) -> None:
        """
        disable frame
        """
        self._change_state("disabled")

class MainMenuFrame(DFrame):
    """
    Main Menu Frame
    """
    def __init__(self, parent, controller: "UIManager"):
        DFrame.__init__(self, parent)

        self.configure(style="MainFrame.TFrame")

        title_lbl = ttk.Label(self, style="Title.TLabel", text="Village Skylines")
        title_lbl.pack(side=tk.TOP, pady=20)

        start_btn = ttk.Button(self,
                               style="Start.TButton",
                               text="Start",
                               command=lambda: controller.change_state(State.IN_GAME))
        start_btn.pack(side=tk.TOP, pady=10)

        quit_btn = ttk.Button(self,
                              style="Quit.TButton",
                              text="Quit",
                              command=controller._call_on_quit)
        quit_btn.pack(side=tk.TOP, pady=10)

class GameFrame(DFrame):
    """
    Game Frame
    """
    def __init__(self, parent, controller: "UIManager"):
        DFrame.__init__(self, parent)

        self._name_lbl = tk.Label(self, text="name_lbl")
        self._name_lbl.pack()

        self._date_lbl = tk.Label(self, text="date_lbl")
        self._date_lbl.pack()

        self._money_lbl = tk.Label(self, text="money_lbl")
        self._money_lbl.pack()

        self._population_lbl = tk.Label(self, text="population_lbl")
        self._population_lbl.pack()

    def update_data(self, village: 'Village') -> None:
        """
        Update displayed data like money_lbl and population_lbl
        """
        self._name_lbl.configure(text=village.name)

        self._date_lbl.configure(text=f"date: {village.get_date_str()}")
        self._money_lbl.configure(text=f"money: {format(village.money, '.2f')}")
        self._population_lbl.configure(text=f"population: {str(village.population)}")

ALL_FRAMES = (MainMenuFrame, GameFrame)
