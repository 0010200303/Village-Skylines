"""
Village Skylines
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import managers.ui_manager
import managers.game_manager
import managers.states

from village import Village

class MainManager:
    """
    Main Manager
    """
    def __init__(self) -> None:
        village = Village.create_village()

        self._current_state = managers.states.State.ERROR

        # set up managers
        self._ui_manager = managers.ui_manager.UIManager(village=village)
        self._game_manager = managers.game_manager.GameManager(village)

        # subscribe to events
        self._ui_manager.subscribe_quit(self.quit)
        self._ui_manager.subscribe_state_changed(self.on_state_changed)
        self._ui_manager.subscribe_key_pressed(self.on_key_pressed)

        self._ui_manager.after(10, self._game_manager.start)
        self._ui_manager.run()

    def quit(self) -> None:
        """
        quit
        """
        self._game_manager.quit()
        self._game_manager.join()

        self._ui_manager.quit()

    def on_state_changed(self, state: managers.states.State) -> None:
        """
        on state changed event
        """
        self._current_state = state

    def on_key_pressed(self, key: str) -> None:
        """
        on key pressed event
        """
        if self._current_state == managers.states.State.IN_GAME:
            match key:
                case "space":
                    self._game_manager.pause()