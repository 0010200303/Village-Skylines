"""
Villager related data classes
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

from jobs import Job

class Villager:
    """
    Villager base class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happines: float) -> None:
        self.name = name
        self.age = age
        self.happiness = happines

class Child(Villager):
    """
    Child class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happiness: float):
        super(Child, self).__init__(name, age, happiness)

class Adult(Villager):
    """
    Adult class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happiness: float,
                 job: Job) -> None:
        super(Adult, self).__init__(name, age, happiness)
        self.job = job

    # TODO: implement full income tax
    @property
    def income_from_tax(self):
        """
        get income from job
        """
        if self.job is None:
            return 0
        return self.job.income * 0.14

class Senior(Villager):
    """
    Senior class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happiness: float) -> None:
        super(Senior, self).__init__(name, age, happiness)
