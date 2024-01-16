"""
Village class
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import random

import constants
from villagers import Villager, Child, Adult, Senior
from jobs import Job

CALLENDER = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class Village:
    """
    Village class
    """
    def __init__(self,
                 start_money: float,
                 villagers: set[Villager],
                 seed: int = 1337,
                 day: int = 1,
                 month: int = 1,
                 year: int = 2024) -> None:
        random.seed(seed)

        self._day = day
        self._month = month
        self._year = year

        self._money = start_money

        self._children = set()
        self._adults = set()
        self._seniors = set()

        for villager in villagers:
            if isinstance(villager, Child):
                self._children.add(villager)
            elif isinstance(villager, Adult):
                self._adults.add(villager)
            elif isinstance(villager, Senior):
                self._seniors.add(villager)
            else:
                if villager.age < constants.ADULT_AGE:
                    self._children.add(Child(villager.name, villager.age, villager.happiness))
                elif villager.age < constants.SENIOR_AGE:
                    self._adults.add(Adult(villager.name, villager.age, villager.happiness, None))
                else:
                    self._seniors.add(Senior(villager.name, villager.age, villager.happiness))

    @classmethod
    def create_village(cls, population_count: int = 10) -> "Village":
        """
        creates standard village
        """
        _villagers = set()
        for i in range(population_count):
            _villagers.add(Adult(str(i), 21 * 365, 100.0, Job("9to5", 16, 8)))

        return cls(10_000, _villagers)

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

    # TODO: implement
    def income_tax(self, money: float) -> float:
        """
        calculate income tax
        """
        return money * 0.14

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

            # TODO: better implementation
            # die
            if random.randint(0, constants.MAX_AGE) <= senior.age:
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
