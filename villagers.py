"""
Villager related data classes
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import io
import struct
from typing import TYPE_CHECKING

from jobs import Job

# includes only needed for typing
if TYPE_CHECKING:
    from buildings import Business

class Villager:
    """
    Villager base class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happines: float) -> None:
        self._name = name
        self.age = age
        self.happiness = happines

    @property
    def name(self) -> str:
        """
        name getter
        """
        return self._name

    def save(self, file: io.BufferedWriter) -> None:
        """
        saves Villager to file
        """
        # name
        file.write(struct.pack(">B", len(self._name )) + bytes(self._name, "utf-8"))

        # age
        file.write(struct.pack(">H", self.age))

        # happiness
        file.write(struct.pack(">f", self.happiness))

    @classmethod
    def load(cls, file: io.BufferedReader) -> "Villager":
        """
        load Villager from file
        """
        return cls(*Villager._load_data(file))

    @staticmethod
    def _load_data(file: io.BufferedReader) -> (str, int, float):
        """
        load villager data from file
        """
        # name
        [temp_length] = struct.unpack(">B", file.read(1))
        name = file.read(temp_length).decode()

        # age
        [age] = struct.unpack(">H", file.read(2))

        # happiness
        [happiness] = struct.unpack(">f", file.read(4))

        return (name, age, happiness)

class Child(Villager):
    """
    Child class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happiness: float):
        super(Child, self).__init__(name, age, happiness)

    def save(self, file: io.BufferedWriter) -> None:
        """
        save Child to file
        """
        super().save(file)

    @classmethod
    def load(cls, file: io.BufferedReader) -> "Child":
        """
        load Child from file
        """
        return cls(*Villager._load_data(file))

class Adult(Villager):
    """
    Adult class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happiness: float,
                 job: Job = None,
                 workplace: "Business" = None) -> None:
        super(Adult, self).__init__(name, age, happiness)
        self._job = job
        self._workplace = workplace

        if self._job is None:
            self._income = 0.0
        else:
            self._income = self._job.income * 0.14

    @property
    def job(self) -> Job:
        """
        job getter
        """
        return self._job

    def set_job(self, job: Job, workplace: "Business" = None) -> None:
        """
        job setter
        """
        self._job = job
        if job is None:
            self._income = 0.0
            self._workplace = None
            return

        self._income = job.income
        self._workplace = workplace

    def loose_job(self) -> None:
        """
        loose job
        """
        if self._workplace is not None:
            self._workplace.loose_job(self)

    # TODO: implement full income tax
    @property
    def income_from_tax(self) -> float:
        """
        get income from job
        """
        return self._income

    def save(self, file: io.BufferedWriter) -> None:
        """
        save Child to file
        """
        super().save(file)

    @classmethod
    def load(cls, file: io.BufferedReader) -> "Adult":
        """
        load Child from file
        """
        return cls(*Villager._load_data(file), None)

class Senior(Villager):
    """
    Senior class
    """
    def __init__(self,
                 name: str,
                 age: int,
                 happiness: float) -> None:
        super(Senior, self).__init__(name, age, happiness)

    def save(self, file: io.BufferedWriter) -> None:
        """
        save Child to file
        """
        super().save(file)

    @classmethod
    def load(cls, file: io.BufferedReader) -> "Senior":
        """
        load Child from file
        """
        return cls(*Villager._load_data(file))
