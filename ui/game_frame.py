"""
Tkinter Game Frame
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ui.frame_base import FrameBase

# includes only needed for typing
if TYPE_CHECKING:
    from managers.main_manager import MainManager
    from village import Village

class GameFrame(FrameBase):
    """
    Game Frame
    """
    def __init__(self, parent, main_manager: "MainManager"):
        FrameBase.__init__(self, parent, main_manager)

        resources_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=1, padx=10, pady=2)

        self._name_lbl = ttk.Label(resources_frame, text="name_lbl")
        self._name_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._date_lbl = ttk.Label(resources_frame, text="date_lbl")
        self._date_lbl.pack(side=tk.RIGHT)

        self._money_img = tk.PhotoImage(file="ui/images/money_icon.png")
        self._money_lbl = ttk.Label(resources_frame,
                                    text="money_lbl",
                                    image=self._money_img,
                                    compound=tk.LEFT)
        self._money_lbl.pack(side=tk.LEFT)

        self._population_img = tk.PhotoImage(file="ui/images/population_icon.png")
        self._population_lbl = ttk.Label(resources_frame,
                                         text="population_lbl",
                                         image=self._population_img,
                                         compound=tk.LEFT)
        self._population_lbl.pack(side=tk.LEFT, padx=(10, 0))

        self._happiness_img = tk.PhotoImage(file="ui/images/happiness_icon.png")
        self._happiness_lbl = ttk.Label(resources_frame,
                                        text="happiness_lbl",
                                        image=self._happiness_img,
                                        compound=tk.LEFT)
        self._happiness_lbl.pack(side=tk.LEFT, padx=(10, 0))

        self._appeal_img = tk.PhotoImage(file="ui/images/appeal_icon.png")
        self._appeal_lbl = ttk.Label(resources_frame,
                                      text="appeal_lbl",
                                      image=self._appeal_img,
                                      compound=tk.LEFT)
        self._appeal_lbl.pack(side=tk.LEFT, padx=(10, 0))

        self._speed_img = tk.PhotoImage(file="ui/images/speed_icon.png")
        self._speed_lbl = ttk.Label(resources_frame,
                                    text="speed_lbl",
                                    image=self._speed_img,
                                    compound=tk.LEFT)
        self._speed_lbl.pack(side=tk.RIGHT, padx=(0, 10))

        resources_frame.pack(side=tk.TOP, fill=tk.X)

    def update_data(self, village: 'Village') -> None:
        """
        Update displayed data like money_lbl and population_lbl
        """
        self._name_lbl.configure(text=village.name)

        self._date_lbl.configure(text=village.get_date_str())
        self._money_lbl.configure(text=format(village.money, '.2f'))
        self._population_lbl.configure(text=str(village.population))
        self._happiness_lbl.configure(text=format(village.total_happiness, '.2f'))
        self._appeal_lbl.configure(text=format(village.appeal, '.2f'))

    def set_speed(self, speed:int) -> None:
        """
        sets current game speed to display
        """
        self._speed_lbl.configure(text=f"{str(speed)}x")
