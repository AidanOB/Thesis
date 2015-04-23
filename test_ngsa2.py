__author__ = "Aidan O'Brien"

"""
This is for testing the sub functions of the ngsa2 implementation that I am writing. It will individually test the
population creation and other sub functions and then the whole function.
"""

from nsga import *

if __name__ == "__main__":
    pop = create_population(20)
    pop2 = create_population(21)
    c_pop = create_child_population(pop)
    c_pop2 = create_child_population(pop2)
    mut_sat = mutate_satellite(c_pop[0], 0)
    # i = 0
    # for sat in c_pop2:
    #     print(i)
    #     i += 1
    #     print(sat)
    R_pop = population_union(pop, c_pop)
    R_pop2 = population_union(pop2, c_pop2)
    sat = calculate_satellite_metrics(R_pop[0])
    print(sat)
