"""
Job related classes
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

import json


class Job:
    """
    Job class
    """
    _initialized = False
    jobs = {}

    def __init__(self,
                 name: str,
                 income: float,
                 payed_by_village: bool = False) -> None:

        self._name = name
        self._income = income
        self._payed_by_village = payed_by_village

        Job.load_jobs()

    @property
    def income(self) -> int:
        """
        income getter
        """
        return self._income

    @property
    def payed_by_village(self) -> bool:
        """
        payed by village getter
        """
        return self._payed_by_village

    @staticmethod
    def load_jobs() -> None:
        """
        load all jobs from file
        """
        if Job._initialized is True:
            return

        Job._initialized = True
        with open("data/jobs.json", encoding="utf-8") as file:
            data = json.load(file)

            # initialize jobs
            for job in data:
                Job.jobs[job["name"]] = Job(name=job.get("name", "unknown job"),
                                             income=job.get("income", 0.0),
                                             payed_by_village=job.get("payed_by_village", False))
