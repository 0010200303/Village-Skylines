"""
Tkinter Load Frame
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import os
import struct
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from typing import TYPE_CHECKING

from ui.frame_base import FrameBase
from managers.states import State

# includes only needed for typing
if TYPE_CHECKING:
    from managers.main_manager import MainManager

class LoadFrame(FrameBase):
    """
    Menu for Loading Game
    """
    def __init__(self, parent, main_manager: "MainManager"):
        FrameBase.__init__(self, parent, main_manager)

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

        columns = ("Name", "last played", "money", "population", "happiness", "appeal", "data")
        for i, text in enumerate(columns):
            self._treeview.heading(i, text=text, command=lambda column=i: \
                                   self._treeview_sort_column(column, False))

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

    def _treeview_sort_column(self, column: int, reverse: bool):
        """
        sort treeview column
        """
        l = [(self._treeview.set(k, column), k) for k in self._treeview.get_children('')]
        l.sort(reverse=reverse)

        for index, (_, k) in enumerate(l):
            self._treeview.move(k, '', index)

        # reverse sort next time
        self._treeview.heading(column, command=lambda: \
                               self._treeview_sort_column(column, not reverse))
