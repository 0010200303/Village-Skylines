"""
Villager related data classes
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import random

import constants
from villagers import Villager, Child, Adult, Senior


class Family:
    """
    Family class
    """
    def __init__(self, villagers: set[Villager]):
        # gets villager
        self._children = {v for v in villagers if isinstance(v, Child)}
        self._adults = {v for v in villagers if isinstance(v, Adult)}
        self._seniors = {v for v in villagers if isinstance(v, Senior)}

        # updates villager in families
        self._children.update([v for v in villagers
                               if type(v) is Villager and v.age < constants.ADULT_AGE])
        self._adults.update([v for v in villagers if
                             type(v) is Villager and v.age < constants.SENIOR_AGE])
        self._seniors.update([v for v in villagers if
                              type(v) is Villager and v.age >= constants.SENIOR_AGE])

        # calculates the people in the family
        self._len = len(self._children) + len(self._adults) + len(self._seniors)

        # calculates the mean happiness
        self._mean_happiness = (sum(child.happiness for child in self._children) +
                                sum(adult.happiness for adult in self._adults) +
                                sum(senior.happiness for senior in self._seniors)) / len(self)
        
        self._house = None

    def __len__(self) -> int:
        return self._len

    @property
    def mean_happiness(self) -> float:
        """
        mean happiness getter
        """
        return self._mean_happiness

    @property
    def unemployed_adults(self) -> set[Adult]:
        """
        unemployed adults getter
        """
        return {adult for adult in self._adults if adult.job is None}

    def tick(self) -> None:
        """
        tick
        """
        children_to_remove = set()
        children_to_add = set()
        seniors_to_remove = set()
        seniors_to_add = set()
        adults_to_remove = set()
        adults_to_add = set()

        # updates attributes for the children
        for child in self._children:
            child.age += 1
            child.happiness -= 0.05

            # lets children grow up
            if child.age >= constants.ADULT_AGE:
                children_to_remove.add(child)
                adults_to_add.add(Adult(child.name, child.age, child.happiness, None))

        # updates attributes for the seniors
        for senior in self._seniors:
            senior.age += 1
            senior.happiness -= 0.05

            # lets seniors die
            if random.randint(0, constants.MAX_AGE) >= 120 - senior.age:
                seniors_to_remove.add(senior)
                self._len -= 1
                continue

        # updates attributes for the adults
        for adult in self._adults:
            adult.age += 1
            adult.happiness -= 0.1

            # lets adults retire
            if adult.age >= constants.SENIOR_AGE:
                adult.set_job(None)

                adults_to_remove.add(adult)
                seniors_to_add.add(Senior(adult.name, adult.age, adult.happiness))

        # update lists
        self._children -= children_to_remove
        self._children.update(children_to_add)

        self._seniors -= seniors_to_remove
        self._seniors.update(seniors_to_add)

        self._adults -= adults_to_remove
        self._adults.update(adults_to_add)

        if len(self) <= 0:
            return

        # calculates the mean happiness
        self._mean_happiness = ((sum(map(lambda child: child.happiness, self._children)) +
                                sum(map(lambda adult: adult.happiness, self._adults)) +
                                sum(map(lambda senior: senior.happiness, self._seniors)))
                                / len(self))

    def set_house(self, house) -> None:
        """
        set house and if null homeless
        """
        if self._house is not None:
            self._house.move_out(self)
        if house is not None:
            house.move_in(self)
        self._house = house

    def leave(self) -> None:
        """
        leave city
        """
        self.set_house(None)

        for adult in self._adults:
            adult.set_job(None)
