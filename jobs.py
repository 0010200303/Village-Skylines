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
                 hours: int,
                 days: int = 20) -> None:
        self._name = name
        self._salary = salary
        self._hours = hours
        self._days = days

    @property
    def income(self) -> int:
        """
        income getter
        """
        return self._salary * self._hours * self._days
