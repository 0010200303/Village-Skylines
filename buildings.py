"""
Building class
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import json

from jobs import Job
from family import Family
from villagers import Adult
import constants


class Building:
    """
    Building class
    """
    _initialized = False
    buildings = []
    houses = []
    businesses = []

    def __init__(self,
                 _id: int,
                 name: str,
                 cost: float = 0.0,
                 appeal: float = 0.0) -> None:
        self._name = name
        self._cost = cost
        self._appeal = appeal

        self._id = _id

        if self._initialized is False:
            Building.load_buildings()

    def __copy__(self) -> "Building":
        print(self._appeal)
        return Building(self._id,
                        self._name,
                        self._cost,
                        self._appeal)

    @property
    def id(self) -> int:
        """
        id getter
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        id setter
        """
        self._id = value

    @property
    def name(self) -> str:
        """
        name getter
        """
        return self._name

    @property
    def cost(self) -> float:
        """
        cost getter
        """
        return self._cost

    @property
    def appeal(self) -> float:
        """
        appeal getter
        """
        return self._appeal

    @staticmethod
    def load_buildings() -> None:
        """
        load all buildings from file
        """
        Building._initialized = True
        with open("data/buildings.json", encoding="utf-8") as file:
            data = json.load(file)

            # initialize general buildings
            Building.buildings = []
            for i, building in enumerate(data["buildings"]):
                Building.buildings.append(Building(i,
                                                   building.get("name", "unknown building"),
                                                   building.get("cost", 0.0),
                                                   building.get("appeal", 0.0)))

            # initialize general houses
            Building.houses = []
            for i, house in enumerate(data["houses"]):
                Building.houses.append(House(i,
                                             house.get("name", "unknown house"),
                                             house.get("cost", 0.0),
                                             house.get("appeal", 0.0)))

            # initialize general businesses
            Building.businesses = []
            for i, business in enumerate(data["businesses"]):
                Building.businesses.append(Business(i,
                                                    business.get("name", "unknown business"),
                                                    business.get("cost", 0.0),
                                                    business.get("appeal", 0.0)))

    @staticmethod
    def copy(building: "Building", _id: int) -> "Building":
        """
        copy building with new id
        """
        return Building(_id,
                        building.name,
                        building.cost,
                        building.appeal)


class House(Building):
    """
    House class
    """
    def __init__(self,
                 _id: int,
                 name: str,
                 cost: float = 0.0,
                 appeal: float = 0.0) -> None:
        super().__init__(_id, name, cost, appeal)

        self._income = 0.0

        self._families = set()

    @property
    def income(self) -> float:
        """
        income getter
        """
        return self._income

    def move_in(self, family: Family) -> None:
        """
        Family move in
        """
        self._families.add(family)

    def move_out(self, family: Family) -> None:
        """
        Family move out
        """
        self._families.remove(family)

    def destroy(self) -> None:
        """
        destroy house and move out all inhabitants
        """
        for family in self._families:
            family.set_house(None)


class Business(Building):
    """
    Business class
    """
    def __init__(self,
                 _id: int,
                 name: str,
                 cost: float = 0.0,
                 appeal: float = 0.0,
                 jobs: {Job: int} = None) -> None:
        super().__init__(_id, name, cost, appeal)

        self.active = True

        self._income = 0.0
        self._running_costs = 0.0
        self._fix_costs = 0.0

        if jobs is None:
            self._open_jobs = {}
        else:
            self._open_jobs = jobs
        self._employees = set()

        self._total_income = self._income - self._running_costs

    @property
    def total_income(self) -> float:
        """
        income getter
        """
        return self._total_income

    @property
    def open_jobs(self) -> {Job: int}:
        """
        jobs getter
        """
        return self._open_jobs

    def try_acquire_job(self, adult: Adult) -> bool:
        """
        tries to acquire an open job from the current business
        """
        # looks if there are any open jobs
        if len(self._open_jobs) <= 0:
            return False

        # gets open job
        job = next(iter(self._open_jobs))
        self._open_jobs[job] -= 1
        if self._open_jobs[job] <= 0:
            self._open_jobs.pop(job)

        # assign the job to an adult
        self._employees.add(adult)
        adult.set_job(job, self)

        # gets income from job
        if job.payed_by_village:
            self._running_costs += job.income
            self._total_income -= job.income

        # gets taxes
        self._income += job.income * constants.INCOME_TAX_PORTION
        self._total_income += job.income * constants.INCOME_TAX_PORTION

        return True

    def loose_job(self, adult: Adult) -> None:
        """
        loose job        
        """
        self._employees.remove(adult)

        if adult.job in self._open_jobs:
            self._open_jobs[adult.job] += 1
        else:
            self._open_jobs[adult.job] = 1

        if adult.job.payed_by_village:
            self._running_costs -= adult.job.income
            self._total_income += adult.job.income

        self._income -= adult.job.income * constants.INCOME_TAX_PORTION
        self._total_income -= adult.job.income * constants.INCOME_TAX_PORTION

    def destroy(self) -> None:
        """
        destroys the business and removes all jobs
        """
        for adult in self._employees:
            adult.set_job(None, destroyed_workplace=True)
