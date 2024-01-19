"""
Village Skylines
"""
__author__ = "8293677, Schoenbrodt, 8288950, Haas"

from managers.main_manager import MainManager


def main() -> None:
    """
    main
    """
    MainManager()

def perf() -> None:
    """
    perfomance test
    """
    import timeit
    from village import Village

    village = Village.create_village("10", population_count=10)
    print(f"pop: 10\t\t\t{timeit.timeit(village.tick, number=1)}")

    village = Village.create_village("1.000", population_count=1_000)
    print(f"pop: 1.000\t\t{timeit.timeit(village.tick, number=1)}")

    village = Village.create_village("100.000", population_count=100_000)
    print(f"pop: 100.000\t\t{timeit.timeit(village.tick, number=1)}")

if __name__ == "__main__":
    main()
    # perf()
