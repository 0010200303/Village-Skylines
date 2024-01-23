"""
UI Manager
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import time
import tkinter as tk

from village import Village

import ui.frames
from managers.states import State

class UIManager(tk.Tk):
    """
    UI Manager
    """
    def __init__(self,
                 *args,
                 main_manager,
                 village: Village,
                 update_rate: float = 1 / 30,
                 **kwargs
                 ) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self._main_manager = main_manager
        self._village = village
        self._running = True
        self._update_rate = update_rate

        self._current_state = State.ERROR



        self.title("Village Sklyines")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self._main_manager.quit)
        self.bind("<KeyPress>", self._call_on_key_pressed)

        self._container = tk.Frame(self)
        self._container.pack(side="top", fill="both", expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        self._current_frame = None

        self._frames = {}
        for t in ui.frames.ALL_FRAMES:
            frame = t(self._container, self._main_manager)

            self._frames[t] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # set up subscripted functions
        self._on_key_pressed_functions = set()

    def change_state(self, state: State) -> None:
        """
        Change current state
        """
        self._current_state = state

        if self._current_frame is not None:
            self._current_frame.disable()

        match state:
            case State.MAIN_MENU:
                self._current_frame = self._frames[ui.frames.MainMenuFrame]
            case State.LOAD_MENU:
                self._current_frame = self._frames[ui.frames.LoadFrame]
            case State.INGAME:
                self._current_frame = self._frames[ui.frames.GameFrame]
            case State.INGAME_MENU:
                self._current_frame = self._frames[ui.frames.IngameMenuFrame]

        self._current_frame.enable()
        self._current_frame.tkraise()

    def set_game_speed(self, speed:int) -> None:
        """
        sets game speed to display
        """
        self._current_frame.set_speed(speed)

    def run(self) -> None:
        """
        main ui loop
        """
        last = 0.0
        while self._running:
            self.update()

            elapsed = time.time() - last
            if elapsed < self._update_rate:
                continue

            self._tick()

            last = time.time()

        # quit
        self.destroy()

    def quit(self) -> None:
        """
        quit
        """
        self._running = False
        print("quitting ui thread")

    def _tick(self) -> None:
        """
        tick
        """
        if self._current_state == State.INGAME:
            self._current_frame.update_data(self._village)

    def _call_on_key_pressed(self, event: tk.Event) -> None:
        """
        Call subscripted functions
        """
        for func in self._on_key_pressed_functions:
            func(event.keysym)

    def subscribe_key_pressed(self, func: callable) -> None:
        """
        Subscribe function to event
        """
        self._on_key_pressed_functions.add(func)
