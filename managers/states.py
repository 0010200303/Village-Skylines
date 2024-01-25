"""
UI States
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

from enum import Enum


class State(Enum):
    """
    State enum
    """
    ERROR = 0
    MAIN_MENU = 1
    LOAD_MENU = 2

    INGAME = 3
    INGAME_MENU = 4
