"""
Village Skylines
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import os

import managers.ui_manager
import managers.game_manager
import managers.states

from village import Village


class MainManager:
    """
    Main Manager
    """
    def __init__(self) -> None:
        village = Village.create_village("Frankfurt", 200)

        self._current_state = managers.states.State.ERROR

        # set up managers
        self._ui_manager = managers.ui_manager.UIManager(main_manager=self, village=village)
        self._game_manager = managers.game_manager.GameManager(main_manager=self, village=village)

        # subscribe to events
        self._ui_manager.subscribe_key_pressed(self.on_key_pressed)

        # open main menu
        self.change_state(state=managers.states.State.MAIN_MENU)

        self._ui_manager.after(10, self._game_manager.start)
        self._ui_manager.run()

    def quit(self) -> None:
        """
        quit
        """
        self._game_manager.quit()
        self._game_manager.join()

        self._ui_manager.quit()

    def change_state(self, state: managers.states.State) -> None:
        """
        change state
        """
        # changes current state
        self._current_state = state
        self._ui_manager.change_state(state)

        # pause game
        if state == managers.states.State.INGAME:
            self._game_manager.pause()
            self.change_game_speed(1)

    def on_key_pressed(self, key: str) -> None:
        """
        on key pressed event
        """
        if self._current_state == managers.states.State.INGAME:
            match key:
                # puts you in the pause menu
                case "Escape":
                    self.change_state(managers.states.State.INGAME_MENU)

                # speed manager
                case "space":
                    self._game_manager.toggle()
                case "1":
                    self.change_game_speed(1)
                case "2":
                    self.change_game_speed(2)
                case "3":
                    self.change_game_speed(5)
                case "4":
                    self.change_game_speed(10)
                case "5":
                    self.change_game_speed(20)
                case "0":
                    self.change_game_speed(10000000)

    def save_game(self) -> None:
        """
        save game to path
        """
        self._game_manager.save()

    def load_game(self, path: str) -> None:
        """
        load game from path
        """
        with open(path, "rb") as file:
            village = Village.load(file)
            self._game_manager._village = village
            self._ui_manager._village = village

            self.change_state(managers.states.State.INGAME)

    def delete_game(self, path: str) -> None:
        """
        delete save game
        """
        if path[-4:] == ".vss":
            os.remove(path)

    def change_game_speed(self, speed: int) -> None:
        """
        change game speed
        """
        self._game_manager.update_rate = 1 / speed
        self._ui_manager.set_game_speed(speed)
