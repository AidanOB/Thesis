__author__ = "Aidan O'Brien"

"""
This module contains all the main code for the genetic algorithm component. It relies on the Non-dominated Sort Genetic
Algorithm-II, NSGA2, to evolve the development of the population.
"""

import random
from components import structures
from components import components as compos
from components import panels
from components import parse_component
import numpy as np
import pandas as pd

MAX_RANDOM_SEARCHES = 10
SIDE_PANELS_TOTAL = 7
NUM_OF_COMPONENTS = len(compos) - 1
NUM_OF_STRUCTURES = len(structures) - 1


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

    structures_pop = [random.randint(0, NUM_OF_STRUCTURES) for _ in range(pop_size)]
    population = []
    for i in range(pop_size):
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
            component_num = random.randint(0, NUM_OF_COMPONENTS)
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

    # for satellite in population:
    #     print(satellite)
    return population


def create_child_population(population):
    """
    This function takes the parent population and creates a population of the same size via combination and
    :param population: 2D array of the same type created in the create_population function
    :return: Returns a 2D array of the same type as create population
    """
    c_pop = []
    # Dividing the population in half, making child satellites pairwise from the two sub-populations
    pop_a = population[:-(int(np.floor(len(population)/2)))]
    pop_b = population[-(int(np.floor(len(population)/2))):]

    if len(pop_a) != len(pop_b):
        spare = pop_a.pop()
    else:
        spare = []

    # Length of pop_a and pop_b will be the same
    # Could refactor the internals of this loop out into dedicated functions, but task for later
    for i in range(len(pop_a)):
        sat_a = {'Structure': pop_a[i]['Structure'],
                 'Components': [],
                 'Panels': [],
                 'Metrics': np.array([], ndmin=1),
                 'Details': np.array([pop_a[i]['Details'][0],
                                      pop_a[i]['Details'][0],
                                      pop_a[i]['Details'][2],
                                      pop_a[i]['Details'][2]], ndmin=1)}
        sat_b = {'Structure': pop_b[i]['Structure'],
                 'Components': [],
                 'Panels': [],
                 'Metrics': np.array([], ndmin=1),
                 'Details': np.array([pop_b[i]['Details'][0],
                                      pop_b[i]['Details'][0],
                                      pop_b[i]['Details'][2],
                                      pop_b[i]['Details'][2]], ndmin=1)}

        comps = []
        for comp in pop_a[i]['Components']:
            comps.append(comp)
        for comp in pop_b[i]['Components']:
            comps.append(comp)

        # Retrieve the number of available slots for each structure
        slots_a = sat_a['Details'][0]
        ext_slots_a = sat_a['Details'][2]
        slots_b = sat_b['Details'][0]
        ext_slots_b = sat_b['Details'][2]

        under_one = MAX_RANDOM_SEARCHES

        while slots_a > 0:
            if comps:
                component = comps.pop(random.randint(0, len(comps) - 1))
                component_num = np.where(compos['Name'] == component)[0][0]

                if slots_a + compos['Internal Slots'][component_num] > 0 \
                        and ext_slots_a + compos['External Slots'][component_num] > 0:
                    sat_a['Components'].append(component)
                    sat_a['Details'][1] += compos['Internal Slots'][component_num]
                    sat_a['Details'][3] += compos['External Slots'][component_num]

                slots_a = sat_a['Details'][1]
                ext_slots_a = sat_a['Details'][3]

                # Less than one counter
                if 0 < slots_a < 1:
                    under_one -= 1

                if under_one < 1:
                    slots_a = 0
            else:
                component_num = random.randint(0, NUM_OF_COMPONENTS)
                component = compos['Name'][component_num]
                if slots_a + compos['Internal Slots'][component_num] > 0 \
                        and ext_slots_a + compos['External Slots'][component_num] > 0:
                    sat_a['Components'].append(component)
                    sat_a['Details'][1] += compos['Internal Slots'][component_num]
                    sat_a['Details'][3] += compos['External Slots'][component_num]

                slots_a = sat_a['Details'][1]
                ext_slots_a = sat_a['Details'][3]
                if 0 < slots_a < 1:
                    under_one -= 1

                if under_one < 1:
                    slots_a = 0
        # Repeat for sat_b
        under_one = MAX_RANDOM_SEARCHES
        while slots_b > 0:
            if comps:
                component = comps.pop(random.randint(0, len(comps) - 1))
                component_num = np.where(compos['Name'] == component)[0][0]

                if slots_b + compos['Internal Slots'][component_num] > 0 \
                        and ext_slots_b + compos['External Slots'][component_num] > 0:
                    sat_b['Components'].append(component)
                    sat_b['Details'][1] += compos['Internal Slots'][component_num]
                    sat_b['Details'][3] += compos['External Slots'][component_num]

                slots_b = sat_b['Details'][1]
                ext_slots_b = sat_b['Details'][3]

                # Less than one counter
                if 0 < slots_b < 1:
                    under_one -= 1

                if under_one < 1:
                    slots_b = 0
            else:
                component_num = random.randint(0, NUM_OF_COMPONENTS)
                component = compos['Name'][component_num]
                if slots_b + compos['Internal Slots'][component_num] > 0 \
                        and ext_slots_b + compos['External Slots'][component_num] > 0:
                    sat_b['Components'].append(component)
                    sat_b['Details'][1] += compos['Internal Slots'][component_num]
                    sat_b['Details'][3] += compos['External Slots'][component_num]

                slots_b = sat_b['Details'][1]
                ext_slots_b = sat_b['Details'][3]
                if 0 < slots_b < 1:
                    under_one -= 1

                if under_one < 1:
                    slots_b = 0

        # Randomly select external panels
        if random.randint(0, 1) == 0:
            sat_a['Panels'] = pop_a[i]['Panels']
            sat_b['Panels'] = pop_b[i]['Panels']
        else:
            sat_a['Panels'] = pop_b[i]['Panels']
            sat_b['Panels'] = pop_a[i]['Panels']

        # append to child population
        c_pop.append(sat_a)
        c_pop.append(sat_b)

    if spare:
        c_pop.append(spare)
    # Return child population
    return c_pop


def mutate_satellite(satellite, structure_mut_rate):
    """
    This function mutates a satellite by generating a new component for the satellite and then filling up the spare
    space with the previous components, dropping the remainder. If a new structure is generated, it fills up the
    available space with previous components and then fills up the remainder with randomly retrieved components
    :param satellite: The satellite to be mutated
    :param structure_mut_rate: The chance that the component to be mutated is the structure
    :return: The mutated satellite
    """

    if random.random() < structure_mut_rate:
        # Structure is mutated
        structure_num = random.randint(0, NUM_OF_STRUCTURES)
        satellite['Structure'] = structures['Name'][structure_num]
        satellite['Details'] = np.array([structures['Internal Slots'][structure_num],
                                         structures['Internal Slots'][structure_num],
                                         structures['External Slots'][structure_num],
                                         structures['External Slots'][structure_num]], ndmin=1)
        new_comp = []
    else:
        new_comp = compos['Name'][random.randint(0, NUM_OF_COMPONENTS)]
    comps = satellite['Components']
    if new_comp:
        comps.append(new_comp)

    satellite['Components'] = []
    available_slots = satellite['Details'][0]
    satellite['Details'][1] = satellite['Details'][0]
    avail_ext_slots = satellite['Details'][2]
    satellite['Details'][3] = satellite['Details'][2]
    under_one = MAX_RANDOM_SEARCHES
    while available_slots > 0:
        if comps:
            component = comps.pop()
            component_num = np.where(compos['Name'] == component)[0][0]
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
        else:
            component_num = random.randint(0, NUM_OF_COMPONENTS)
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
    # Clearing the metrics, since they will be different
    satellite['Metrics'] = np.array([], ndmin=1)
    return satellite


def population_union(population_one, population_two):
    """
    This function takes two populations and makes a union of the two into a greater cohesive population.
    :param population_one: A population of any size
    :param population_two: A different population of any size
    :return: P_1 U P_2
    """
    return population_one + population_two


def calculate_satellite_metrics(satellite):
    """
    This function takes a satellite structure that has been created and evaluates the metrics that it possesses, it
    updates the Metrics array in the satellite before returning it
    :param satellite: The satellite structure
    :return: The satellite structure with the metrics array calculated
    """

    comps = satellite['Components']
    for comp in comps:
        comp_num = np.where(compos['Name'] == comp)[0][0]
        print(pd.DataFrame(compos.loc[comp_num]))
        metrics_sums, metrics_mins, metrics_max, sum_vals, max_vals = parse_component(pd.DataFrame(compos.loc[comp_num]))
        # print(metrics_sums)


def parse_component(component):
    """
    Parses the component utilising values that are required for the genetic algorithm, returning raw values that can be
    converted into appropriate metrics later
    :param component: Pandas series entry for the component
    :return: raw values in a numpy array
    """
    pass