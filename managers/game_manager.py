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
    def __init__(self, village: Village, update_rate: float = 1 / 100000) -> None:
        threading.Thread.__init__(self)
        self.__stop = False

        self._village = village
        self._running = False
        self._update_rate = update_rate

    def run(self) -> None:
        """
        run
        """
        last = 0.0
        while not self.__stop:
            while self._running:
                elapsed = time.time() - last
                if elapsed < self._update_rate:
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
        self._running = not self._running

    def save(self) -> None:
        """
        saves the current game
        """
        with open("saves/tust.vss", "wb") as file:
            self._village.save(file)
        print("saved game!")
