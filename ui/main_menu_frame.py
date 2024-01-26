"""
Tkinter Main Menu Frame
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


class MainMenuFrame(FrameBase):
    """
    Main Menu Frame
    """
    def __init__(self, parent, main_manager: "MainManager", village: "Village"):
        FrameBase.__init__(self, parent, main_manager, village)

        self.configure(style="DefaultFrame.TFrame")

        # title label
        title_lbl = ttk.Label(self, style="Title.TLabel", text="Village Skylines")
        title_lbl.pack(side=tk.TOP, pady=20)

        # start button
        start_btn = ttk.Button(self,
                               style="MainMenu.TButton",
                               text="Start",
                               command=lambda: self._main_manager.change_state(State.INGAME))
        start_btn.pack(side=tk.TOP, pady=10)

        # load button
        load_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Load",
                              command=lambda: self._main_manager.change_state(State.LOAD_MENU))
        load_btn.pack(side=tk.TOP, pady=10)

        # quit button
        quit_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Quit",
                              command=self._main_manager.quit)
        quit_btn.pack(side=tk.TOP, pady=10)
