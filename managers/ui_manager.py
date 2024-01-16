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
                 village: Village,
                 pull_rate: float = 1 / 30,
                 **kwargs
                 ) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self._village = village
        self._running = True
        self._pull_rate = pull_rate



        self.title("Village Sklyines")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self._call_on_quit)
        self.bind("<KeyPress>", self._call_on_key_pressed)

        self._container = tk.Frame(self)
        self._container.pack(side="top", fill="both", expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        self._current_frame = None

        self._frames = {}
        for t in ui.frames.ALL_FRAMES:
            frame = t(self._container, self)

            self._frames[t] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # set up subscripted functions
        self._on_quit_functions = set()
        self._on_state_changed_functions = set()
        self._on_key_pressed_functions = set()

        self.change_state(State.MAIN_MENU)

    def change_state(self, state: State) -> None:
        """
        Change current state
        """
        self._current_state = state
        match state:
            case State.MAIN_MENU:
                frame = self._frames[ui.frames.MainMenuFrame]
            case State.IN_GAME:
                frame = self._frames[ui.frames.GameFrame]

        if self._current_frame is not None:
            self._current_frame.disable()

        frame.enable()
        frame.tkraise()
        self._current_frame = frame
        self._call_on_state_changed(state)

    def run(self) -> None:
        """
        main ui loop
        """
        last = 0.0
        while self._running:
            self.update()

            elapsed = time.time() - last
            if elapsed < self._pull_rate:
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
        if self._current_state == State.IN_GAME:
            self._current_frame.update_data(self._village)

    def _call_on_quit(self) -> None:
        """
        Call subscripted functions
        """
        for func in self._on_quit_functions:
            func()

    def subscribe_quit(self, func: callable) -> None:
        """
        assign function to quit event
        """
        self._on_quit_functions.add(func)

    def _call_on_state_changed(self, state: State) -> None:
        """
        Call subscripted functions
        """
        for func in self._on_state_changed_functions:
            func(state)

    def subscribe_state_changed(self, func: callable) -> None:
        """
        Subscribe function to event
        """
        self._on_state_changed_functions.add(func)

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
