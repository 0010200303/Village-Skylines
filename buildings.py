"""
Building class
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

from jobs import Job
from villagers import Adult

class Building:
    """
    Building class
    """
    def __init__(self, name: str, area: (int, int), position: (int, int)) -> None:
        self._name = name
        self._area = area
        self._position = position

class House(Building):
    """
    House class
    """
    def __init__(self, name: str, area: (int, int), position: (int, int)) -> None:
        super().__init__(name, area, position)

        self._income = self._area[0] * self._area[1]

    @property
    def income(self) -> float:
        """
        income getter
        """
        return self._income

class Business(Building):
    """
    Business class
    """
    def __init__(self,
                 name: str,
                 area: (int, int),
                 position: (int, int),
                 jobs: {Job: int} = None) -> None:
        super().__init__(name, area, position)

        self._income = self._area[0] * self._area[1] * 2.0
        self._fix_costs = self._area[0] * self._area[1] * 0.5
        self.active = True

        if jobs is None:
            self._open_jobs = {}
        else:
            self._open_jobs = jobs
        self._employees = set()
        self._job_costs = 0.0

        self._total_income = self._income - self._fix_costs + self._job_costs

    @property
    def income(self) -> float:
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
        tries to aquire an open job from the current business
        """
        if len(self._open_jobs) <= 0:
            return False

        job = next(iter(self._open_jobs))
        self._open_jobs[job] -= 1
        if self._open_jobs[job] <= 0:
            self._open_jobs.pop(job)

        self._employees.add(adult)

        adult.set_job(job, self)

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

    def destroy(self) -> None:
        """
        destroys the business and removes all jobs
        """
        for adult in self._employees:
            adult.set_job(None)
