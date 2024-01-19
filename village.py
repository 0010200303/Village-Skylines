"""
Village class
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import random
import io
import struct

import constants
from villagers import Villager, Child, Adult, Senior
from buildings import Building, House, Business
from jobs import Job

CALLENDER = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class Village:
    """
    Village class
    """
    def __init__(self,
                 name: str,
                 start_money: float,
                 villagers: set[Villager],
                 buildings: set[Building],
                 day: int = 1,
                 month: int = 1,
                 year: int = 2024,
                 seed: int = 1337) -> None:
        random.seed(seed)

        self._name = name
        self._money = start_money

        self._children = {v for v in villagers if isinstance(v, Child)}
        self._adults = {v for v in villagers if isinstance(v, Adult)}
        self._seniors = {v for v in villagers if isinstance(v, Senior)}

        self._children.update([v for v in villagers \
                               if type(v) is Villager and v.age < constants.ADULT_AGE])
        self._adults.update([v for v in villagers if \
                             type(v) is Villager and v.age < constants.SENIOR_AGE])
        self._seniors.update([v for v in villagers if \
                              type(v) is Village and v.age >= constants.SENIOR_AGE])

        self._houses = {b for b in buildings if isinstance(b, House)}
        self._businesses = {b for b in buildings if isinstance(b, Business)}

        self._day = day
        self._month = month
        self._year = year

    @classmethod
    def create_village(cls, name: str, population_count: int = 10) -> "Village":
        """
        creates standard village
        """
        villagers = {Adult(str(i), 21 * 365, 100.0, Job("9to5", 16, 8)) for i in range(population_count)}
        buildings = set()
        buildings.update({House(str(i), (10, 10), (0, 0)) for i in range(population_count // 4)})
        buildings.update({Business(str(i), (10, 10), (0, 0)) for i in range(population_count // 100)})

        return cls(name, 10_000, villagers, buildings)

    @property
    def name(self) -> str:
        """
        name getter
        """
        return self._name

    @property
    def money(self) -> float:
        """
        money getter
        """
        return self._money

    @property
    def population(self) -> int:
        """
        population getter
        """
        return len(self._children) + len(self._adults) + len(self._seniors)

    def get_date_str(self) -> str:
        """
        returns the current date as a string
        """
        return f"{str(self._day)}.{str(self._month)}.{self._year}"

    def income_tax(self, money: float) -> float:
        """
        calculate income tax
        """
        return money * 0.14

    def save(self, file: io.BufferedWriter) -> None:
        """
        save village to file
        """
        # name
        file.write(struct.pack(">B", len(self._name)) + bytes(self._name, "utf-8"))

        # money
        file.write(struct.pack(">d", self._money))

        # children
        file.write(struct.pack(">i", len(self._children)))
        for child in self._children:
            child.save(file)

        # adults
        file.write(struct.pack(">i", len(self._adults)))
        for adult in self._adults:
            adult.save(file)

        # seniors
        file.write(struct.pack(">i", len(self._seniors)))
        for senior in self._seniors:
            senior.save(file)

        # date
        file.write(struct.pack(">BBI", self._day, self._month, self._year))

        # TODO: save random state

    @classmethod
    def load(cls, file: io.BufferedReader) -> "Village":
        """
        load Village from file
        """
        # name
        [temp_length] = struct.unpack(">B", file.read(1))
        name = file.read(temp_length).decode()

        # money
        [money] = struct.unpack(">d", file.read(8))

        villagers = []
        # children
        [children_count] = struct.unpack(">i", file.read(4))
        villagers.extend([Child.load(file) for _ in range(children_count)])

        # adults
        [adult_count] = struct.unpack(">i", file.read(4))
        villagers.extend([Adult.load(file) for _ in range(adult_count)])

        # seniors
        [senior_count] = struct.unpack(">i", file.read(4))
        villagers.extend([Senior.load(file) for _ in range(senior_count)])

        # date
        [day, month, year] = struct.unpack(">BBI", file.read(6))

        return cls(name, money, villagers, day, month, year)

    def tick(self) -> None:
        """
        tick
        """
        self._tick_day()
        if self._day > CALLENDER[self._month - 1]:
            self._day = 1

            self._tick_month()
            if self._month > 12:
                self._month = 1

                self._year += 1

    def _tick_day(self) -> None:
        """
        day tick
        """
        self._day += 1

        children_to_remove = set()
        children_to_add = set()
        seniors_to_remove = set()
        seniors_to_add = set()
        adults_to_remove = set()
        adults_to_add = set()

        for child in self._children:
            child.age += 1
            child.happiness -= 0.05

            # grow up
            if child.age >= constants.ADULT_AGE:
                children_to_remove.add(child)
                adults_to_add.add(Adult(child.name, child.age, child.happiness, None))

        for senior in self._seniors:
            senior.age += 1
            senior.happiness -= 0.05

            # die
            if random.randint(0, constants.MAX_AGE) >= 120 - senior.age:
                seniors_to_remove.add(senior)
                continue

        for adult in self._adults:
            adult.age += 1
            adult.happiness -= 0.1

            # leave
            if adult.happiness <= constants.MIN_HAPPINESS:
                adults_to_remove.add(adult)
                continue

            # pension
            if adult.age >= constants.SENIOR_AGE:
                adults_to_remove.add(adult)
                seniors_to_add.add(Senior(adult.name, adult.age, adult.happiness))

        for business in self._businesses:
            if random.random() > 0.99:
                business.active = False

        # update lists
        self._children -= children_to_remove
        self._children.update(children_to_add)

        self._seniors -= seniors_to_remove
        self._seniors.update(seniors_to_add)

        self._adults -= adults_to_remove
        self._adults.update(adults_to_add)

    def _tick_month(self) -> None:
        """
        month tick
        """
        self._month += 1

        self._money += sum(adult.income_from_tax for adult in self._adults) \
                        * constants.INCOME_TAX_PORTION

        self._money += sum(house.income for house in self._houses)
        self._money += sum(business.income for business in self._businesses if business.active)
