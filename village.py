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
from villagers import Villager, Child, Adult, Senior
from buildings import Building, House, Business

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

        self._buildings = {b.id: b for b in buildings if isinstance(b, House) is False
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
        Building.load_buildings()

        village = cls(name, 10_000, set(), set(), day=27)

        # create houses
        for _ in range(20):
            village.buy_building(Building.houses[0], True)
        for _ in range(11):
            village.buy_building(Building.houses[1], True)
        for _ in range(2):
            village.buy_building(Building.houses[2], True)

        # create businesses
        for _ in range(2):
            village.buy_building(Building.businesses[0], True)

        # create villagers
        village._gain_new_families(population_count)

        return village

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
        calculates the mean happiness from all villager
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
        file.write(struct.pack(">Iff", self.population, self.mean_happiness, self.appeal))

        # families
        file.write(struct.pack(">I", len(self._families)))
        for family in self._families:
            family.save(file)

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
        file.read(12)

        # families
        villagers = []

        return cls(name, money, villagers, [], day, month, year)

    def tick(self) -> None:
        """
        tick
        """
        # one day
        self._tick_day()

        # one month
        if self._day > CALLENDER[self._month - 1]:
            self._day = 1

            self._tick_month()

            # one year
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
                              if family.mean_happiness <= constants.MIN_HAPPINESS \
                              or len(family) <= 0}
        self._families -= families_to_remove
        for family in families_to_remove:
            family.leave()

        # update businesses
        for business in self._businesses.values():
            if random.random() > 0.99:
                business.active = False

        # find new home
        for family in self._families:
            if family.house is None:
                house = self._find_house(len(family))

                if house is not None:
                    family.set_house(house)

        # gain new families
        self._gain_new_families()

    def _find_house(self, capacity: int) -> House:
        """
        find house with enough capacity for family else return None
        """
        for house in self._houses.values():
            if house.free_capacity >= capacity:
                return house
        return None

    def _gain_new_families(self, person_count: int = None) -> None:
        """
        gain new family
        """
        if person_count is None:
            if self.population <= 0:
                return
            person_count = (self.appeal / self.population) * self.mean_happiness

        while True:
            child_count = int(random.triangular(0, 5, 2))
            adult_count = int(random.triangular(1, 5, 1.8))
            senior_count = int(random.triangular(0, 3, 1.3))
            total = child_count + adult_count + senior_count

            if total > person_count:
                break

            # check if any house has enough capacity for family
            house = self._find_house(total)

            person_count -= total

            last_name = random.choice(Villager.last_names)

            villagers = set()
            villagers.update({Child(f"{random.choice(Villager.first_names)} \
                                    {last_name}", \
                                    random.triangular(0, 17 * 365, 10 * 365), \
                                    random.triangular(0, 100, 80)) for i in range(child_count)})
            villagers.update({Adult(f"{random.choice(Villager.first_names)} \
                                    {last_name}", \
                                    random.triangular(18 * 365, 75 * 365, 32 * 365), \
                                    random.triangular(0, 100, 80)) for i in range(adult_count)})
            villagers.update({Senior(f"{random.choice(Villager.first_names)} \
                                    {last_name}", \
                                    random.triangular(80 * 365, 119 * 365, 100 * 365), \
                                    random.triangular(0, 100, 80)) for i in range(senior_count)})

            family = Family(villagers)
            family.set_house(house)

            self._families.add(family)

    def _tick_month(self) -> None:
        """
        month tick
        """
        self._month += 1

        # updates money
        self._money -= sum(building.running_costs for building in self._buildings.values())
        self._money -= sum(house.running_costs for house in self._houses.values())
        self._money += sum(business.total_income for business in self._businesses.values())

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
                list_ = self._buildings
            case "<class \'buildings.House\'>":
                list_ = self._houses
            case "<class \'buildings.Business\'>":
                list_ = self._businesses

        building = list_.pop(building_id)

        if isinstance(building, Business):
            building.destroy()

        self._appeal -= building.appeal

    def buy_building(self, building: Building, init: bool = False) -> Building:
        """
        buying building
        """
        if self._money < building.cost:
            return None

        # subtract cost of building
        if init is False:
            self._money -= building.cost

        new_building = copy.copy(building)

        # looks what building has to be build
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
