"""
Tkinter Ingame Menu Frame
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ui.frame_base import FrameBase
from managers.states import State

# includes only needed for typing
if TYPE_CHECKING:
    from managers.main_manager import MainManager
    from village import Village

class IngameMenuFrame(FrameBase):
    """
    Ingame Menu
    """
    def __init__(self, parent, main_manager: "MainManager", village: "Village"):
        FrameBase.__init__(self, parent, main_manager, village)

        self.configure(style="MainFrame.TFrame")

        title_lbl = ttk.Label(self, style="Title.TLabel", text="Pause")
        title_lbl.pack(side=tk.TOP, pady=20)

        continue_btn = ttk.Button(self,
                                  style="MainMenu.TButton",
                                  text="Continue",
                                  command=lambda: self._main_manager.change_state(State.INGAME))
        continue_btn.pack(side=tk.TOP, padx=10, pady=10)

        save_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Save",
                              command=self._main_manager.save_game)
        save_btn.pack(side=tk.TOP, padx=10, pady=10)

        exit_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Exit",
                              command=lambda: self._main_manager.change_state(State.MAIN_MENU))
        exit_btn.pack(side=tk.TOP, padx=10, pady=10)

        quit_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Quit",
                              command=self._main_manager.quit)
        quit_btn.pack(side=tk.TOP, padx=10, pady=10)
