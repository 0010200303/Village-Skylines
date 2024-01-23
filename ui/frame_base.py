"""
Tkinter Frame Base
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

# includes only needed for typing
if TYPE_CHECKING:
    from managers.main_manager import MainManager

class FrameBase(ttk.Frame):
    """
    Frame that can be disable and enabled
    """
    style = None

    def __init__(self, parent, main_manager: "MainManager"):
        ttk.Frame.__init__(self, parent)
        self._main_manager = main_manager

        if self.style is None:
            self.style = ttk.Style()
            self.style.configure("MainFrame.TFrame",
                                 background="pink")
            self.style.configure("Title.TLabel",
                                 foreground="Purple",
                                 background="pink",
                                 font=("Comic Sans ms", 72))
            self.style.configure("MainMenu.TButton",
                                 font=("Comic Sans MS", 16),
                                 borderwidth=8,
                                 relief=tk.RAISED)

    def _change_state(self, state: str) -> None:
        """
        Changes state of all widgets
        """
        for child in self.winfo_children():
            if isinstance(child, ttk.Button):
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
