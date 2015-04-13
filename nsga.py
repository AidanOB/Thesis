__author__ = "Aidan O'Brien"

"""
This module contains all the main code for the genetic algorithm component. It relies on the Non-dominated Sort Genetic
Algorithm-II, NSGA2, to evolve the development of the population.
"""

MAX_RANDOM_SEARCHES = 10
SIDE_PANELS_TOTAL = 7

import random
from components import structures
from components import components as compos
from components import panels
import numpy as np


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
    num_of_components = len(compos) - 1
    structures_pop = [random.randint(0, num_of_structures) for _ in range(pop_size)]
    population = []
    for i in range(pop_size):
        # print(structures['Name'][structures_pop[i]])  # Proof of successful access
        # print(structures['Internal Slots'][structures_pop[i]])
        satellite = {'Structure': structures['Name'][structures_pop[i]],
                     'Components': [],
                     'Panels': [],
                     'Metrics': np.array([], ndmin=1),
                     'Details': np.array([structures['Internal Slots'][structures_pop[i]],
                                          structures['Internal Slots'][structures_pop[i]],
                                          structures['External Slots'][structures_pop[i]],
                                          structures['External Slots'][structures_pop[i]]], ndmin=1)}

        available_slots = satellite['Details'][1]
        avail_ext_slots = satellite['Details'][3]
        under_one = MAX_RANDOM_SEARCHES
        while available_slots > 0:
            component_num = random.randint(0, num_of_components)
            component = compos['Name'][component_num]
            if available_slots + compos['Internal Slots'][component_num] > 0 \
                    and avail_ext_slots + compos['External Slots'][component_num] > 0:
                satellite['Components'].append(component)
                satellite['Details'][1] += compos['Internal Slots'][component_num]
                satellite['Details'][3] += compos['External Slots'][component_num]
            available_slots = satellite['Details'][1]
            avail_ext_slots = satellite['Details'][3]

            if 0 < available_slots < 1:
                under_one -= 1

            if under_one < 1:
                available_slots = 0

        side_panel = panels['Name'][random.randint(0, SIDE_PANELS_TOTAL-1)]
        end_panel = panels['Name'][random.randint(SIDE_PANELS_TOTAL, len(panels) - 1)]
        satellite['Panels'].append([side_panel, end_panel])
        # Append the current satellite to the population
        population.append(satellite)

    for satellite in population:
        print(satellite)


def create_child_population(population):
    """
    This function takes the parent population and creates a population of the same size via combination and
    :param population: 2D array of the same type created in the create_population function
    :return: Returns a 2D array of the same type as create population
    """
    pass


