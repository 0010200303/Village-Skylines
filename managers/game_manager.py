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
    def __init__(self, village: Village) -> None:
        threading.Thread.__init__(self)
        self.__stop = False

        self._village = village
        self._running = False

    def run(self) -> None:
        """
        run
        """
        last = 0.0
        while not self.__stop:
            while self._running:
                elapsed = time.time() - last
                if elapsed < 1.0:
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
