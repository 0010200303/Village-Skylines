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
                 hours: int) -> None:
        self._name = name
        self._salary = salary
        self._hours = hours

    @property
    def income(self) -> int:
        """
        income getter
        """
        return self._salary * self._hours
