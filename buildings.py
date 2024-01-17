"""
Building class
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

class Building:
    """
    Building class
    """
    def __init__(self, name: str, area: (int, int), position: (int, int)) -> None:
        self._name = name
        self._area = area
        self._position = position

class House(Building):
    """
    House class
    """
    def __init__(self, name: str, area: (int, int), position: (int, int)) -> None:
        super().__init__(name, area, position)

        self._income = self._area[0] * self._area[1]

    @property
    def income(self) -> float:
        """
        income getter
        """
        return self._income

class Business(Building):
    """
    Business class
    """
    def __init__(self, name: str, area: (int, int), position: (int, int)) -> None:
        super().__init__(name, area, position)

        self._income = self._area[0] * self._area[1] * 2.0
        self._costs = self._area[0] * self._area[1] * 0.5
        self.active = True

    @property
    def income(self) -> float:
        """
        income getter
        """
        return self._income

    @property
    def costs(self) -> float:
        """
        costs getter
        """
        return self._costs
