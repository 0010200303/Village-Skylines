"""
Tkinter Game Frame
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ui.frame_base import FrameBase
from buildings import Building, House, Business

# includes only needed for typing
if TYPE_CHECKING:
    from managers.main_manager import MainManager
    from village import Village

class GameFrame(FrameBase):
    """
    Game Frame
    """
    def __init__(self, parent, main_manager: "MainManager", village: "Village"):
        FrameBase.__init__(self, parent, main_manager, village)

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



        vertical_paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        horizontal_paned_window = ttk.PanedWindow(vertical_paned_window, orient=tk.HORIZONTAL)
        vertical_paned_window.pack(fill=tk.BOTH, expand=True)
        horizontal_paned_window.pack(fill=tk.BOTH, expand=True)
        vertical_paned_window.add(horizontal_paned_window)

        # info frame
        info_frame = ttk.Frame(vertical_paned_window, style="MainFrame.TFrame")
        info_frame.pack(fill=tk.BOTH, expand=True)

        self._building_info = ttk.Label(info_frame)
        self._building_info.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

        self._destroy_btn = ttk.Button(info_frame, text="Destroy", state=tk.DISABLED)
        self._destroy_btn.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

        vertical_paned_window.add(info_frame)

        # buildings frame
        buildings_frame = ttk.Frame(horizontal_paned_window, style="MainFrame.TFrame")
        buildings_frame.pack(fill=tk.BOTH, expand=True)

        buildings_lbl = ttk.Label(buildings_frame, text="Village Buldings")
        buildings_lbl.pack(side=tk.TOP)

        columns = ("type", "name")
        buildings_scrollbar = ttk.Scrollbar(buildings_frame)
        self._buildings_list = ttk.Treeview(buildings_frame,
                                            yscrollcommand=buildings_scrollbar.set,
                                            selectmode=tk.BROWSE,
                                            show="headings",
                                            columns=columns)
        buildings_scrollbar.configure(command=self._buildings_list.yview)

        self._buildings_list.bind("<<TreeviewSelect>>", self._display_building)

        for i, text in enumerate(columns):
            self._buildings_list.heading(i, text=text, command=lambda column=i: \
                                    self._treeview_sort_column(self._buildings_list, column, False))

        for building in self._village._buildings.values():
            values = ("building", building.name)
            self._buildings_list.insert("", tk.END, tags=(Building, building.id), values=values)

        for house in self._village.houses.values():
            values = ("house", house.name)
            self._buildings_list.insert("", tk.END, tags=(House, house.id), values=values)

        for business in self._village.businesses.values():
            values = ("business", business.name)
            self._buildings_list.insert("", tk.END, tags=(Business, business.id), values=values)

        buildings_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self._buildings_list.pack(fill=tk.BOTH, expand=True)

        horizontal_paned_window.add(buildings_frame, weight=30)

        # shop frame
        shop_frame = ttk.Frame(horizontal_paned_window, style="MainFrame.TFrame")
        shop_frame.pack(fill=tk.BOTH, expand=True)

        shop_lbl = ttk.Label(shop_frame, text="Shop")
        shop_lbl.pack(side=tk.TOP)

        columns = ("type", "name")
        shop_scrollbar = ttk.Scrollbar(shop_frame)
        self._shop_list = ttk.Treeview(shop_frame,
                                       yscrollcommand=shop_scrollbar.set,
                                       selectmode=tk.BROWSE,
                                       show="headings",
                                       columns=columns)
        shop_scrollbar.configure(command=self._shop_list.yview)

        self._shop_list.bind("<<TreeviewSelect>>", self._display_shop)

        for i, text in enumerate(columns):
            self._shop_list.heading(i, text=text, command=lambda column=i: \
                              self._treeview_sort_column(self._shop_list, column, False))

        for building in Building.buildings:
            values = ("building", building.name)
            self._shop_list.insert("", tk.END, tags=(Building, building.id), values=values)

        for house in Building.houses:
            values = ("house", house.name)
            self._shop_list.insert("", tk.END, tags=(House, house.id), values=values)

        for business in Building.businesses:
            values = ("business", business.name)
            self._shop_list.insert("", tk.END, tags=(Business, business.id), values=values)

        shop_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self._shop_list.pack(fill=tk.BOTH, expand=True)

        horizontal_paned_window.add(shop_frame, weight=30)

        # shop info frame
        shop_info_frame = ttk.Frame(horizontal_paned_window, style="MainFrame.TFrame")
        shop_info_frame.pack(fill=tk.BOTH, expand=True)

        shop_info_title_lbl = ttk.Label(shop_info_frame, text="Shop Info")
        shop_info_title_lbl.pack(side=tk.TOP)

        self._shop_info_lbl = ttk.Label(shop_info_frame)
        self._shop_info_lbl.pack(side=tk. TOP, anchor=tk.NW, padx=4, pady=4)

        self._buy_btn = ttk.Button(shop_info_frame, text="Buy", state=tk.DISABLED)
        self._buy_btn.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

        horizontal_paned_window.add(shop_info_frame, weight=1)

    def update_data(self) -> None:
        """
        Update displayed data to labels like money_lbl and population_lbl
        """
        self._name_lbl.configure(text=self._village.name)

        self._date_lbl.configure(text=self._village.get_date_str())
        self._money_lbl.configure(text=format(self._village.money, '.2f'))
        self._population_lbl.configure(text=str(self._village.population))
        self._happiness_lbl.configure(text=format(self._village.mean_happiness, '.2f'))
        self._appeal_lbl.configure(text=format(self._village.appeal, '.2f'))

    def set_speed(self, speed:int) -> None:
        """
        sets current game speed to display
        """
        self._speed_lbl.configure(text=f"{str(speed)}x")

    def _display_building(self, _event: tk.Event) -> None:
        """
        displays information of a building
        """
        if len(self._buildings_list.selection()) <= 0:
            return

        building_type, building_id = self._buildings_list.item(\
            self._buildings_list.selection()[0], "tags")
        building_id = int(building_id)

        self._destroy_btn.configure(state=tk.NORMAL, command=lambda: \
                                    self._destroy_building(self._buildings_list.selection()[0]))

        match building_type:
            case "<class \'buildings.Building\'>":
                building = self._village.buildings[building_id]

                text = f"Name: {building.name}"
            case "<class \'buildings.House\'>":
                house = self._village.houses[building_id]

                text = f"Name: {house.name}"
            case "<class \'buildings.Business\'>":
                business = self._village.businesses[building_id]

                text = f"Name: {business.name}"

        self._building_info.configure(text=text)

    def _destroy_building(self, selection) -> None:
        """
        destroy building
        """
        building_type, building_id = self._buildings_list.item(selection)["tags"]
        building_id = int(building_id)

        match building_type:
            case "<class \'buildings.Building\'>":
                l = self._village.buildings
            case "<class \'buildings.House\'>":
                l = self._village.houses
            case "<class \'buildings.Business\'>":
                l = self._village.businesses

        self._village.destroy_building(building_type, building_id)
        self._buildings_list.delete(selection)

        # clear frame
        self._destroy_btn.configure(state=tk.DISABLED, command=None)
        self._building_info.configure(text="")

    def _display_shop(self, _event: tk.Event) -> None:
        """
        display bulding from shop
        """
        if len(self._shop_list.selection()) <= 0:
            return

        building_type, building_id = self._shop_list.item(self._shop_list.selection()[0], "tags")
        building_id = int(building_id)

        self._buy_btn.configure(state=tk.NORMAL, command=lambda: \
                                self._buy_building(self._shop_list.selection()[0]))

        match building_type:
            case "<class \'buildings.Building\'>":
                building = Building.buildings[building_id]

                text = f"Name: {building.name}"
            case "<class \'buildings.House\'>":
                house = Building.houses[building_id]

                text = f"Name: {house.name}"
            case "<class \'buildings.Business\'>":
                business = Building.businesses[building_id]

                text = f"Name: {business.name}"

        self._shop_info_lbl.configure(text=text)

    def _buy_building(self, selection) -> None:
        """
        buy building
        """
        building_type, building_id = self._shop_list.item(selection)["tags"]
        building_id = int(building_id)

        match building_type:
            case "<class \'buildings.Building\'>":
                building = Building.buildings[building_id]
            case "<class \'buildings.House\'>":
                building = Building.houses[building_id]
            case "<class \'buildings.Business\'>":
                building = Building.businesses[building_id]

        if (building := self._village.buy_building(building)) is None:
            return

        values = ("building", building.name)
        self._buildings_list.insert("", tk.END, tags=(Building, building.id), values=values)
