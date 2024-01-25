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
    from village import Village


class FrameBase(ttk.Frame):
    """
    Frame that can be disabled and enabled
    """
    style = None

    def __init__(self, parent, main_manager: "MainManager", village: "Village"):
        ttk.Frame.__init__(self, parent)
        self._main_manager = main_manager
        self._village = village

        # sets styles
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

    def _treeview_sort_column(self, treeview: ttk.Treeview, column: int, reverse: bool):
        """
        sort treeview column
        """
        list_ = [(treeview.item(k, 'values')[column], k) for k in treeview.get_children('')]
        list_.sort(reverse=reverse)

        for index, (_, k) in enumerate(list_):
            treeview.move(k, '', index)

        # reverse sort next time
        treeview.heading(column, command=lambda:
                         self._treeview_sort_column(treeview, column, not reverse))
