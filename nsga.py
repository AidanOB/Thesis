__author__ = "Aidan O'Brien"

"""
This module contains all the main code for the genetic algorithm component. It relies on the Non-dominated Sort Genetic
Algorithm-II, NSGA2, to evolve the development of the population.
"""

import random
from components import structures


def create_population(pop_size):
    """
    This is a function utilised to create the initial population
    :param pop_size: Determines how large a sample of population should be created
    :return: Returns 2D array of potential satellite configurations, 1 dimension is the satellites, the second is the
     components that make up the satellite
    """
    # Making the population. Create the initial array each with a random structure chosen. Then each structure filled
    # out with components. Random internals, random externals.
    # Gather the number of possible types of structures, this changes with the db and create a vector of the randomly
    # generated structures to utilise

    num_of_structures = len(structures) - 1
    structures_pop = [random.randint(0, num_of_structures) for _ in range(pop_size)]
    for i in range(pop_size):
        print(structures['Name'][structures_pop[i]])  # Proof of successful access




def create_child_population(population):
    """
    This function takes the parent population and creates a population of the same size via combination and
    :param population: 2D array of the same type created in the create_population function
    :return: Returns a 2D array of the same type as create population
    """
    pass


