__author__ = "Aidan O'Brien"

"""
This is for testing the sub functions of the ngsa2 implementation that I am writing. It will individually test the
population creation and other sub functions and then the whole function.
"""

from nsga import *
import matplotlib.pyplot as plt
import time
import utils

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
    # print(sat)

    targets = np.array([0.334, 0.5, 0.334, 0.5, 0.334])
    for j in range(len(R_pop)):
        R_pop[j] = calculate_satellite_metrics(R_pop[j])
        R_pop[j]['ID'] = j

    R_pop = calculate_fitness(R_pop, targets)
    calculate_rankings(R_pop)
    new_pop = []
    for satellite in R_pop:
        # print(satellite['Rank'])
        if satellite['Rank'] < 20:
            new_pop.append(satellite)

    # Test the genetic algorithm
    print('Starting Genetic Algorithm')
    t = time.time()
    final_pop, perf = genetic_algorithm(100, 100, 0.3, targets)
    elapsed_time = time.time() - t
    print('Elapsed Time: ' + str(elapsed_time) + 's')
    print(final_pop[0]['Fitness'])
    print(perf)

    utils.plot_ga_performance(perf, '')