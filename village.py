"""
Village class
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import random
import io
import struct
import copy

import constants
from family import Family
from villagers import Child, Adult, Senior
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
                 families: set[Family],
                 buildings: set[Building],
                 day: int = 1,
                 month: int = 1,
                 year: int = 2024,
                 seed: int = 1337) -> None:
        random.seed(seed)

        self._name = name
        self._money = start_money

        self._families = families

        self._buildings = {b.id: b for b in buildings if isinstance(b, House) is False \
                           and isinstance(b, Business) is False}
        self._houses = {b.id: b for b in buildings if isinstance(b, House)}
        self._businesses = {b.id: b for b in buildings if isinstance(b, Business)}

        self._day = day
        self._month = month
        self._year = year

        self._appeal = 0.0
        for building in self._buildings.values():
            self._appeal += building.appeal
        for house in self._houses.values():
            self._appeal += house.appeal
        for business in self._businesses.values():
            self._appeal += business.appeal

    @classmethod
    def create_village(cls, name: str, population_count: int = 10) -> "Village":
        """
        creates standard village
        """
        families = {Family({Adult(f"Generic{str(j)}", 21 * 365, 100.0, None) for j in range(2)}) \
                    for i in range(population_count // 2)}

        jobs = {Job("9to5", 16, 8, 20): 4}

        buildings = set()
        buildings.update({House(i, str(i)) for i in range(population_count // 4)})
        buildings.update({Business(i, str(i), jobs=dict(jobs)) \
                          for i in range(population_count // 100)})

        return cls(name, 10_000, families, buildings, day=30)

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
        return sum(len(family) for family in self._families)

    @property
    def mean_happiness(self) -> float:
        """
        total happiness getter
        """
        if len(self._families) <= 0:
            return 0.0

        return sum(family.mean_happiness for family in self._families) / len(self._families)

    @property
    def appeal(self) -> float:
        """
        appeal getter
        """
        return self._appeal

    @property
    def buildings(self) -> set[Building]:
        """
        buildings getter
        """
        return self._buildings

    @property
    def houses(self) -> set[House]:
        """
        houses getter
        """
        return self._houses

    @property
    def businesses(self) -> set[Business]:
        """
        businesses
        """
        return self._businesses

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

        # date
        file.write(struct.pack(">BBI", self._day, self._month, self._year))

        # preview stats
        file.write(struct.pack(">iff", self.population, self.mean_happiness, self.appeal))

        # families
        # file.write(struct.pack(">i", len(self._children)))
        # file.write(struct.pack(">i", len(self._adults)))
        # file.write(struct.pack(">i", len(self._seniors)))

        # for child in self._children:
        #     child.save(file)

        # for adult in self._adults:
        #     adult.save(file)

        # for senior in self._seniors:
        #     senior.save(file)

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

        # date
        [day, month, year] = struct.unpack(">BBI", file.read(6))

        # skip preview stats
        file.read(8)

        # villagers
        villagers = []

        [children_count] = struct.unpack(">i", file.read(4))
        [adult_count] = struct.unpack(">i", file.read(4))
        [senior_count] = struct.unpack(">i", file.read(4))

        villagers.extend([Child.load(file) for _ in range(children_count)])
        villagers.extend([Adult.load(file) for _ in range(adult_count)])
        villagers.extend([Senior.load(file) for _ in range(senior_count)])

        return cls(name, money, villagers, [], day, month, year)

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

        # update families
        list(map(lambda family: family.tick(), self._families))

        # remove families
        families_to_remove = {family for family in self._families \
                              if family.mean_happiness <= constants.MIN_HAPPINESS}
        self._families -= families_to_remove

        # update businesses
        for business in self._businesses.values():
            if random.random() > 0.99:
                business.active = False

    def _tick_month(self) -> None:
        """
        month tick
        """
        self._month += 1

        self._money += sum(house.income for house in self._houses.values())
        self._money += sum(business.total_income for business in self._businesses.values() \
                           if business.active)

        # adults find job
        for family in self._families:
            for adult in family.unemployed_adults:
                for business in self._businesses.values():
                    if business.try_acquire_job(adult) is True:
                        break

    def destroy_building(self, building_type: str, building_id: int) -> None:
        """
        destroy building
        """
        match building_type:
            case "<class \'buildings.Building\'>":
                l = self._buildings
            case "<class \'buildings.House\'>":
                l = self._houses
            case "<class \'buildings.Business\'>":
                l = self._businesses
        building = l.pop(building_id)
        if isinstance(building, Business):
            building.destroy()

        self._appeal -= building.appeal

    def buy_building(self, building: Building) -> Building:
        """
        buy building
        """
        if self._money < building.cost:
            return None

        self._money -= building.cost

        new_building = copy.copy(building)

        if isinstance(new_building, House):
            new_building.id = len(self._houses)
            self._houses[new_building.id] = new_building
        elif isinstance(new_building,  Business):
            new_building.id = len(self._businesses)
            self._businesses[new_building.id] = new_building
        else:
            new_building.id = len(self._buildings)
            self._buildings[new_building.id] = new_building

        self._appeal += new_building.appeal

        return new_building
