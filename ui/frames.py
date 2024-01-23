"""
Tkinter Frames
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import os
import struct
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from PIL import ImageTk, Image

from managers.states import State

# includes only needed for typing
if TYPE_CHECKING:
    from managers.main_manager import MainManager
    from village import Village

class DFrame(ttk.Frame):
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

class MainMenuFrame(DFrame):
    """
    Main Menu Frame
    """
    def __init__(self, parent, main_manager: "MainManager"):
        DFrame.__init__(self, parent, main_manager)

        self.configure(style="MainFrame.TFrame")

        title_lbl = ttk.Label(self, style="Title.TLabel", text="Village Skylines")
        title_lbl.pack(side=tk.TOP, pady=20)

        start_btn = ttk.Button(self,
                               style="MainMenu.TButton",
                               text="Start",
                               command=lambda: self._main_manager.change_state(State.INGAME))
        start_btn.pack(side=tk.TOP, pady=10)

        load_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Load",
                              command=lambda: self._main_manager.change_state(State.LOAD_MENU))
        load_btn.pack(side=tk.TOP, pady=10)

        quit_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Quit",
                              command=self._main_manager.quit)
        quit_btn.pack(side=tk.TOP, pady=10)

class LoadFrame(DFrame):
    """
    Menu for Loading Game
    """
    def __init__(self, parent, main_manager: "MainManager"):
        DFrame.__init__(self, parent, main_manager)

        self.configure(padding=(10, 10))

        tree_frame = ttk.Frame(self)

        scrollbar = ttk.Scrollbar(tree_frame)
        self._treeview = ttk.Treeview(tree_frame,
                                yscrollcommand=scrollbar.set,
                                selectmode=tk.BROWSE,
                                show="headings",
                                columns=("name",
                                         "money",
                                         "population",
                                         "happiness",
                                         "appeal",
                                         "date",
                                         "last played"))
        scrollbar.configure(command=self._treeview.yview)

        self._treeview.bind("<Double-1>", self._load_game)

        self._treeview.heading(0, text="Name")
        self._treeview.heading(1, text="last played")
        self._treeview.heading(2, text="money")
        self._treeview.heading(3, text="population")
        self._treeview.heading(4, text="happiness")
        self._treeview.heading(5, text="appeal")
        self._treeview.heading(6, text="date")

        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self._treeview.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        back_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Back",
                              command=lambda: self._main_manager.change_state(State.MAIN_MENU))
        back_btn.pack(side=tk.LEFT, anchor=tk.SW, pady=(10, 0))

        delete_btn = ttk.Button(self,
                                style="MainMenu.TButton",
                                text="Delete",
                                command=self._delete_game)
        delete_btn.pack(side=tk.LEFT, anchor=tk.SW, padx=(10, 0), pady=(10, 0))

        load_btn = ttk.Button(self,
                              style="MainMenu.TButton",
                              text="Load",
                              command=lambda: self._load_game(None))
        load_btn.pack(side=tk.RIGHT, anchor=tk.SE, pady=(10, 0))

    def enable(self) -> None:
        """
        enable frame and load preview for files
        """
        super().enable()

        self._treeview.delete(*self._treeview.get_children())

        for path in os.listdir("saves"):
            path = "saves/" + path
            if path[-4:] != ".vss":
                continue

            # load save game preview
            with open(path, "rb") as file:
                # name
                [temp_length] = struct.unpack(">B", file.read(1))
                name = file.read(temp_length).decode()

                # money
                [money] = struct.unpack(">d", file.read(8))

                # date
                [day, month, year] = struct.unpack(">BBI", file.read(6))

                # happiness and appeal
                [happiness, appeal] = struct.unpack(">ff", file.read(8))

                # villagers
                villager_count = sum(struct.unpack(">iii", file.read(12)))

                last_played = datetime.fromtimestamp(os.path.getmtime(path))

                values = (name,
                          last_played.strftime("%d.%m.%Y %H:%M"),
                          format(money, '.2f'),
                          villager_count,
                          str(format(happiness, '.2f')),
                          str(format(appeal, '.2f')),
                          f"{day}.{month}.{year}")
                self._treeview.insert("", tk.END, text=path, values=values)

    def _load_game(self, _event: tk.Event) -> None:
        """
        load selected game
        """
        if len(self._treeview.selection()) <= 0:
            return

        path = self._treeview.item(self._treeview.selection()[0], "text")
        self._main_manager.load_game(path)

    def _delete_game(self) -> None:
        """
        delete selected game
        """
        if (len(self._treeview.selection())) <= 0:
            return

        path = self._treeview.item(self._treeview.selection()[0], "text")
        self._main_manager.delete_game(path)

        self._treeview.delete(self._treeview.selection())

class GameFrame(DFrame):
    """
    Game Frame
    """
    def __init__(self, parent, main_manager: "MainManager"):
        DFrame.__init__(self, parent, main_manager)

        resources_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=1, padx=10, pady=2)

        self._name_lbl = ttk.Label(resources_frame, text="name_lbl")
        self._name_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._date_lbl = ttk.Label(resources_frame, text="date_lbl")
        self._date_lbl.pack(side=tk.RIGHT)

        self._money_img = ImageTk.PhotoImage(Image.open("ui/images/money_icon.png"))
        self._money_lbl = ttk.Label(resources_frame,
                                    text="money_lbl",
                                    image=self._money_img,
                                    compound=tk.LEFT)
        self._money_lbl.pack(side=tk.LEFT)

        self._population_img = ImageTk.PhotoImage(Image.open("ui/images/population_icon.png"))
        self._population_lbl = ttk.Label(resources_frame,
                                         text="population_lbl",
                                         image=self._population_img,
                                         compound=tk.LEFT)
        self._population_lbl.pack(side=tk.LEFT, padx=(10, 0))

        self._happiness_img = ImageTk.PhotoImage(Image.open("ui/images/happiness_icon.png"))
        self._happiness_lbl = ttk.Label(resources_frame,
                                        text="happiness_lbl",
                                        image=self._happiness_img,
                                        compound=tk.LEFT)
        self._happiness_lbl.pack(side=tk.LEFT, padx=(10, 0))

        self._appeal_img = ImageTk.PhotoImage(Image.open("ui/images/appeal_icon.png"))
        self._appeal_lbl = ttk.Label(resources_frame,
                                      text="appeal_lbl",
                                      image=self._appeal_img,
                                      compound=tk.LEFT)
        self._appeal_lbl.pack(side=tk.LEFT, padx=(10, 0))

        self._speed_img = ImageTk.PhotoImage(Image.open("ui/images/speed_icon.png"))
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

class IngameMenuFrame(DFrame):
    """
    Ingame Menu
    """
    def __init__(self, parent, main_manager: "MainManager"):
        DFrame.__init__(self, parent, main_manager)

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

ALL_FRAMES = (MainMenuFrame, LoadFrame, GameFrame, IngameMenuFrame)
