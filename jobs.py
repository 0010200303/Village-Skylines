"""
Job related classes
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"


class Job:
    """
    Job class
    """
    def __init__(self,
                 name: str,
                 salary: int,
                 hours: int = 8,
                 days: int = 20,
                 payed_by_village: bool = False) -> None:

        self._name = name
        self._salary = salary
        self._hours = hours
        self._days = days
        self._payed_by_village = payed_by_village

    @property
    def income(self) -> int:
        """
        income getter
        """
        return self._salary * self._hours * self._days

    @property
    def payed_by_village(self) -> bool:
        """
        payed by village getter
        """
        return self._payed_by_village
