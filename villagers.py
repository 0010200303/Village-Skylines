"""
Villager related data classes
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import io
import struct
from typing import TYPE_CHECKING

from jobs import Job
import constants

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
                 job_id: str = None,
                 workplace: "Business" = None) -> None:
        super(Adult, self).__init__(name, age, happiness)

        Job.load_jobs()

        self._job_id = job_id
        self._workplace = workplace

        # checks if adult has job and sets the tax
        if self._job_id is None:
            self._income = 0.0
        else:
            self._income = Job.jobs[self._job_id].income * constants.INCOME_TAX_PORTION

    @property
    def job_id(self) -> Job:
        """
        job getter
        """
        return self._job_id

    @property
    def income_from_tax(self) -> float:
        """
        get income from job
        """
        return self._income

    def set_job(self,
                job_id: str,
                workplace: "Business" = None,
                destroyed_workplace: bool = False) -> None:
        """
        job setter
        """
        if job_id is None:
            self._income = 0.0

            if destroyed_workplace is False and self._workplace is not None:
                self._workplace.loose_job(self)
        else:
            self._income = Job.jobs[job_id].income * constants.INCOME_TAX_PORTION

        self._job_id = job_id
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
