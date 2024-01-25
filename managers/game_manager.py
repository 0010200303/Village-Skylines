"""
Game Manager
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import threading
import time

from village import Village

class GameManager(threading.Thread):
    """
    Game Manager
    """
    def __init__(self,
                 main_manager,
                 village: Village,
                 update_rate: float = 1 / 1) -> None:
        threading.Thread.__init__(self)
        self.__stop = False

        self._main_manager = main_manager
        self._village = village
        self._running = False
        self.update_rate = update_rate

    def run(self) -> None:
        """
        run
        """
        last = 0.0
        while not self.__stop:
            while self._running:
                elapsed = time.time() - last
                if elapsed < self.update_rate:
                    continue

                self._tick()

                last = time.time()

    def quit(self) -> None:
        """
        quit
        """
        self._running = False
        self.__stop = True
        print("quitting game thread")

    def _tick(self) -> None:
        """
        tick
        """
        self._village.tick()

    def pause(self) -> None:
        """
        pause the game
        """
        self._running = False

    def continue_(self) -> None:
        """
        continue the game
        """
        self._running = True

    def toggle(self) -> None:
        """
        toggle running the game
        """
        self._running = not self._running

    def save(self) -> None:
        """
        saves the current game
        """
        with open(f"saves/{self._village.name}.vss", "wb") as file:
            self._village.save(file)
        print(f"saved game to saves/{self._village.name}.vss!")
