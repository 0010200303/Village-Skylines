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
    _initialized = False
    first_names = ["Firstname"]
    last_names = ["Lastname"]

    def __init__(self,
                 name: str,
                 age: int,
                 happines: float) -> None:
        self._name = name
        self.age = age
        self.happiness = happines

        Villager.load_names()

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
        file.write(struct.pack(">B", len(self._name)) + bytes(self._name, "utf-8"))

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

    @staticmethod
    def load_names() -> None:
        """
        load names
        """
        if Villager._initialized is True:
            return
        Villager._initialized = True

        with open("data/first_names.txt", encoding="utf-8") as file:
            Villager.first_names = file.read().splitlines()
        with open("data/last_names.txt", encoding="utf-8") as file:
            Villager.last_names = file.read().splitlines()

class Child(Villager):
    """
    Child class
    """
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

        # checks if adult has job and sets the tax
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

    @property
    def income_from_tax(self) -> float:
        """
        get income from job
        """
        return self._income

    def set_job(self,
                job: Job,
                workplace: "Business" = None,
                destroyed_workplace: bool = False) -> None:
        """
        job setter
        """
        if job is None:
            self._income = 0.0

            if destroyed_workplace is False and self._workplace is not None:
                self._workplace.loose_job(self)
        else:
            self._income = job.income

        self._job = job
        self._workplace = workplace

    def save(self, file: io.BufferedWriter) -> None:
        """
        save Adult to file
        """
        super().save(file)

    @classmethod
    def load(cls, file: io.BufferedReader) -> "Adult":
        """
        load Adult from file
        """
        return cls(*Villager._load_data(file), None)


class Senior(Villager):
    """
    Senior class
    """
    @classmethod
    def load(cls, file: io.BufferedReader) -> "Senior":
        """
        load Senior from file
        """
        return cls(*Villager._load_data(file))
