__author__ = "Aidan O'Brien"

"""
This module contains all the main code for the genetic algorithm component. It relies on the Non-dominated Sort Genetic
Algorithm-II, NSGA2, to evolve the development of the population.
"""

import random
from components import structures
from components import components as compos
from components import panels
from components import calculate_cpu_metric
from components import calculate_br_down_metric, calculate_br_up_metric, calculate_wavelength_metric

# from components import parse_component
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
                     'Fitness': np.array([], ndmin=1),
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
                 'Fitness': np.array([], ndmin=1),
                 'Details': np.array([pop_a[i]['Details'][0],
                                      pop_a[i]['Details'][0],
                                      pop_a[i]['Details'][2],
                                      pop_a[i]['Details'][2]], ndmin=1)}
        sat_b = {'Structure': pop_b[i]['Structure'],
                 'Components': [],
                 'Panels': [],
                 'Metrics': np.array([], ndmin=1),
                 'Fitness': np.array([], ndmin=1),
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
    # print(satellite)
    size = pd.DataFrame(structures.loc[np.where(structures['Name'] ==
                                                satellite['Structure'])[0][0]]).T['Size'].values[0]
    comps = satellite['Components']
    values = np.array([])
    for comp in comps:
        comp_num = np.where(compos['Name'] == comp)[0][0]
        if not values.any():
            values = parse_component(pd.DataFrame(compos.loc[comp_num]).T)
        else:
            values = np.vstack((values, parse_component(pd.DataFrame(compos.loc[comp_num]).T)))

    # print(values)
    combined = combine_values(values)

    structure_values = parse_component(pd.DataFrame(structures.loc[np.where(structures['Name']
                                                                            == satellite['Structure'])[0][0]]).T)
    panels_values = np.array([])
    for panel in satellite['Panels'][0]:
        panel_num = np.where(panels['Name'] == panel)[0][0]
        if not panels_values.any():
            panels_values = parse_component(pd.DataFrame(panels.loc[panel_num]).T)
        else:
            panels_values = np.vstack((panels_values, parse_component(pd.DataFrame(panels.loc[panel_num]).T)))

    raw_values = combine_sections(structure_values, combined, panels_values, size)
    # [mass, max_power, min_wavelength, max_wavelength, detail, br_down, br_up, data, code, ram,
    # att_know, att_mom, price, discharge]
    volume_met = volume_metric(structure_values[0], combined[0])
    mass_met = mass_metric(size, raw_values[0])
    cpu_met = calculate_cpu_metric(raw_values[7], raw_values[8], raw_values[9])
    power_met = power_metric(raw_values[-1], raw_values[1], 1)
    br_down_met = calculate_br_down_metric(raw_values[5])
    br_up_met = calculate_br_up_metric(raw_values[6])
    wavelength_met = calculate_wavelength_metric(raw_values[2], raw_values[3])
    att_met = att_moment_metric(raw_values[0], raw_values[11])
    att_know_met = att_know_metric(raw_values[10])
    wave_det_met = raw_values[4]

    satellite['Metrics'] = np.array([volume_met, mass_met, cpu_met, power_met, br_down_met, br_up_met, att_met,
                                     att_know_met, wavelength_met, wave_det_met])

    return satellite


def att_know_metric(att_knowledge):
    """
    This calculates the attitude knowledge metric from the given value
    :param att_knowledge: The accuracy that can be determined for the satellite
    :return:
    """
    if att_knowledge < 10e-5:
        return 0

    modded_know = 18 / att_knowledge

    if modded_know == 1:
        remainder = 0
        cr_tiers = 1
    elif modded_know < 1:
        if modded_know > 0.75:
            cr_tiers = modded_know
        else:
            cr_tiers = 0
        remainder = 0
    else:
        cr_tiers = 1
        while modded_know > 1:
            cr_tiers += 1
            modded_know /= 3

        if modded_know != 1:
            remainder = np.mod(1 - modded_know, 3)
        else:
            remainder = 0

    cr_gap_distance = 1 / 6

    return np.float64(cr_tiers * cr_gap_distance - remainder * cr_gap_distance).clip(min=0, max=1)


def parse_component(component):
    """
    Parses the component utilising values that are required for the genetic algorithm, returning raw values that can be
    converted into appropriate metrics later
    :param component: Pandas series entry for the component
    :return: raw values in a numpy array
    """

    volume = (component['X'] * component['Y'] * component['Z']).values[0]
    mass = component['Mass'].values[0]
    nom_power = component['Nom Power'].values[0]
    max_power = component['Power (W)'].values[0] - nom_power
    min_wavelength = component['Min Wavelength (nm)'].values[0]
    max_wavelength = component['Max Wavelength (nm)'].values[0]
    detail = component['Resolution'].values[0]
    br_down = component['Bit Rate Down'].values[0]
    br_up = component['Bit Rate Up'].values[0]
    data = component['Data Storage (MB)'].values[0]
    code = component['Code Storage (MB)'].values[0]
    ram = component['RAM'].values[0]
    att_know = component['Attitude Know (deg)'].values[0]
    att_mom = component['Attitude Control moment'].values[0]
    discharge = component['Discharge Time (Wh)'].values[0]
    price = component['Price ($US)'].values[0]

    values = np.array([volume, mass, nom_power, max_power, min_wavelength, max_wavelength, detail, br_down, br_up, data,
                       code, ram, att_know, att_mom, discharge, price])
    return values


def combine_values(value_array):
    """
    Takes in a numpy array of the values for the satellite and parses them into the required values for metric
    conversion
    :param value_array: numpy array
    :return: numpy vector
    """

    volume = np.sum(value_array[:, 0], axis=0)
    mass = np.sum(value_array[:, 1], axis=0)
    max_power = np.sum(value_array[:, 2], axis=0) + np.max(value_array[:, 3], axis=0)
    # Hard decision for the choice of average wavelength, could go with an average of the two and hope for
    # mutation/child to remove an item, or to take either or. Will leave it up to random to decide
    min_wavelength = np.min(value_array[:, 4], axis=0)
    max_wavelength = np.max(value_array[:, 5], axis=0)
    # Detail is pre-calculated into a metric
    detail = np.max(value_array[:, 6], axis=0)
    br_down = np.max(value_array[:, 7], axis=0)
    br_up = np.max(value_array[:, 8], axis=0)
    data = np.sum(value_array[:, 9], axis=0)
    code = np.sum(value_array[:, 10], axis=0)
    ram = np.sum(value_array[:, 11], axis=0)
    att_temp = value_array[:, 12]
    att_temp = att_temp[att_temp > 0]
    # att_know = np.min(value_array[:, 12], axis=0)  # minimum value is best, not calculating combination of sources
    if att_temp.any():
        att_know = np.min(att_temp, axis=0)
    else:
        att_know = 0
    att_mom = np.sum(value_array[:, 13], axis=0)  # Straight summation rather than more complicated algorithms since
    # distribution of masses is unknown
    discharge = np.sum(value_array[:, 14], axis=0)
    price = np.sum(value_array[:, 15], axis=0)

    combined_values = np.array([volume, mass, max_power, min_wavelength, max_wavelength, detail, br_down, br_up, data,
                                code, ram, att_know, att_mom, price, discharge])
    return combined_values


def combine_sections(structure_vals, component_vals, panel_vals, size):
    """

    :param structure_vals:
    :param component_vals:
    :param panel_vals:
    :return:
    """
    mass = np.sum(structure_vals[1]) + np.sum(component_vals[1]) + 4 * np.sum(panel_vals[:, 1], axis=0) * size
    max_power = np.sum(structure_vals[2]) + np.sum(component_vals[2]) + 4 * np.sum(panel_vals[:, 2], axis=0) * size
    min_wavelength = component_vals[3]
    max_wavelength = component_vals[4]
    detail = component_vals[5]
    br_down = component_vals[6]
    br_up = component_vals[7]
    data = component_vals[8] + structure_vals[8]
    code = component_vals[9] + structure_vals[9]
    ram = component_vals[10] + structure_vals[10]
    att_temp = np.array([structure_vals[11], component_vals[11], panel_vals[0, 11], panel_vals[1, 11]])
    att_temp = att_temp[att_temp > 0]
    if att_temp.any():
        att_know = np.min(att_temp)
    else:
        att_know = 0
    att_mom = np.sum(np.array([structure_vals[12], component_vals[12], panel_vals[0, 12] * 4 * size, panel_vals[0, 12]]))
    price = structure_vals[13] + component_vals[13] + 4 * np.sum(panel_vals[:, 13], axis=0) * size
    discharge = structure_vals[14] + component_vals[14] + 4 * np.sum(panel_vals[:, 14], axis=0) * size

    combined_sections = np.array([mass, max_power, min_wavelength, max_wavelength, detail, br_down, br_up, data, code,
                                  ram, att_know, att_mom, price, discharge])
    return combined_sections


def volume_metric(max_volume, combined_volumes):
    """
    This function calculates the volume metric
    :param max_volume: The maximum allowed internal volume
    :param combined_volumes: the volume for all the internal components
    :return: the calculated metric for the volume.
    """
    vol = max_volume - combined_volumes
    if vol < 0:
        penalty = np.exp(-vol) - 1
    else:
        penalty = 0

    return np.float64(1 - penalty).clip(min=0, max=1)


def mass_metric(sat_size, sat_mass):
    """
    This function calculates the metric for the mass of the satellite based upon the maximum allowed for its size.
    :param sat_size: Either 1, 1.5, 2 or 3, to correlate to CubeSat sizes of 1U, 1.5U, 2U and 3U
    :param sat_mass: the total mass of the satellite including all peripherals
    :return: The metric value
    """

    if sat_size == 1:
        allowed = 1.33
    elif sat_size == 1.5:
        allowed = 2
    elif sat_size == 2:
        allowed = 2.66
    elif sat_size == 3:
        allowed = 4
    else:
        allowed = 1.33 * sat_size

    mass = allowed - sat_mass

    if mass < 0:
        penalty = np.exp(-mass) - 1
    else:
        penalty = 0

    return np.float64(1 - penalty).clip(min=0, max=1)


def power_metric(discharge, power, batt_required):
    """
    This calculates the metric for the power requirements for the satellite.
    :param discharge: This is a value for the battery discharge time. If a battery is required then this will be
    utilised
    :param power: The maximum power usage, whether or not the satellite can run all the components on board
    :param batt_required: A bool value decided for a whole population
    :return: power metric, a value between 0 and 1
    """

    if discharge > 0:
        has_batt = True
    else:
        has_batt = False

    if power < 0:
        penalty = np.exp(-power) - 1
    else:
        penalty = 0

    metric = 1 - penalty

    if batt_required and not has_batt:
        metric /= 2

    return metric


def att_moment_metric(mass, att_moment):
    """
    This function calculates the metric for the attitude moment. It does not consider moments of inertia for the
    satellite, nor passive sources of moment
    :param mass:
    :param att_moment:
    :return:
    """
    return np.float64(1.25 * (att_moment / mass)).clip(min=0, max=1)


def genetic_algorithm(generations, pop_size, mut_rate, target_reqs):
    if pop_size < 15:
        pop_size = 15

    population = create_population(pop_size)

    # Put a history logging array here
    performance_data = np.array([np.nan, np.nan, np.nan])

    for i in range(generations):
        # if not i % 10:
        print("Starting generation: " + str(i))
        # Create a child population
        child_pop = create_child_population(population)

        # Provide a chance of mutating an individual satellite in the child population
        for j in range(pop_size):
            if random.random() < mut_rate:
                child_pop[j] = mutate_satellite(child_pop[j], mut_rate)

        # Create the union of the parent and child populations. Size is now 2*pop_size
        r_pop = population_union(population, child_pop)

        # Calculate the metrics for the satellite
        for j in range(len(r_pop)):
            r_pop[j] = calculate_satellite_metrics(r_pop[j])
            r_pop[j]['ID'] = j

        # Calculate the distances from the desired requirements. The first four are always volume, mass, cpu and power
        r_pop = calculate_fitness(r_pop, target_reqs)

        # Calculate the rank of all the members within the population, based on the number of zero distances, then the
        # minimum distances to break ties where the same number of zeros are found. In second tier ties, randomly select
        # an order. Ensure at least one with a minimum value for each CR limits are always included at the top of the
        # rankings.
        pop2, max_zeros = calculate_rankings(r_pop)

        # Place the satellites in order of rank into a new population until n == pop_size
        new_pop = []

        for satellite in pop2:
            # print(satellite['Rank'])
            if satellite['Rank'] < pop_size:
                new_pop.append(satellite)

        # Calculate and save this generations performance
        average_dist, min_dist = performance(new_pop)
        gen_performance = np.array([max_zeros, average_dist, min_dist])
        performance_data = np.vstack((performance_data, gen_performance))

        # Start loop again
        population = new_pop

    # Return the population and generations details.
    performance_data = performance_data[~np.isnan(performance_data).any(1)]
    return population, performance_data


def performance(population):
    values = np.array([np.nan, np.nan])

    for j in range(len(population)):
        num_zeros = np.sum(population[j]['Fitness'] == 0)
        total_dist = np.sum(population[j]['Fitness'])
        values = np.vstack((values, np.array([num_zeros, total_dist])))

    values = values[~np.isnan(values).any(1)]

    average_dist = np.sum(values[:, 1]) / len(population)
    min_dist = np.min(values[:, 1])

    return average_dist, min_dist


def calculate_rankings(population):
    """

    :param population:
    :return:
    """
    # for satellite in population:
    #     print(satellite)
    values = np.array([np.nan, np.nan])
    non_sum = np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
    # Finding the number of zero values
    cur_rank = 0
    for j in range(len(population)):
        num_zeros = np.sum(population[j]['Fitness'] < 10e-14)
        total_dist = np.sum(population[j]['Fitness'])
        values = np.vstack((values, np.array([num_zeros, total_dist])))
        non_sum = np.vstack((non_sum, population[j]['Fitness']))

    values = values[~np.isnan(values).any(1)]
    non_sum = non_sum[~np.isnan(non_sum).any(1)]

    average_dist = np.sum(values[:, 1]) / len(population)
    min_dist = np.min(values[:, 1])
    max_zeros = np.max(values[:, 0])

    population[np.where(min_dist == values[:, 1])[0][0]]['Rank'] = cur_rank
    values[np.where(min_dist == values[:, 1])[0][0]] = -1
    cur_rank += 1

    for i in range(10):
        population[np.where(non_sum[:, i] == np.min(non_sum[:, i]))[0][0]]['Rank'] = cur_rank
        values[np.where(non_sum[:, i] == np.min(non_sum[:, i]))[0][0]] = -1
        non_sum[np.where(non_sum[:, i] == np.min(non_sum[:, i]))[0][0]] = 10
        cur_rank += 1

    while np.max(values[:, 0]) >= 0:
        locs = np.where(values[:, 0] == np.max(values[:, 0]))[0]
        vals_sorted = np.sort(values[locs, 1])

        for j in range(len(vals_sorted)):
            population[locs[np.where(values[locs, 1] == vals_sorted[j])[0][0]]]['Rank'] = cur_rank
            values[locs[np.where(values[locs, 1] == vals_sorted[j])[0][0]]] = -1
            cur_rank += 1

        values[locs] = -1

    return population, max_zeros


def calculate_fitness(population, targets):
    """
    This function goes through an entire population and calculates the individuals fitness compared to the target goals
    along with some constant targets
    :param population: A population of satellites
    :param targets:
    :return:
    """
    # The goal values are constants for satellites to operate effectively and within requirements, the customer reqs
    # are the same and are covered by the targets
    volume_goal = 1
    mass_goal = 1
    cpu_goal = 1
    power_goal = 1
    br_down_goal = targets[0]
    br_up_goal = targets[1]
    att_mom_goal = targets[2]
    att_know_goal = targets[2]
    wave_goal = targets[3]
    wave_det_goal = targets[4]

    for satellite in population:
        vol_fit = good_enough_distance(volume_goal, satellite['Metrics'][0])
        mass_fit = good_enough_distance(mass_goal, satellite['Metrics'][1])
        cpu_fit = good_enough_distance(cpu_goal, satellite['Metrics'][2])
        power_fit = good_enough_distance(power_goal, satellite['Metrics'][3])
        br_d_fit = good_enough_distance(br_down_goal, satellite['Metrics'][4])
        br_u_fit = good_enough_distance(br_up_goal, satellite['Metrics'][5])
        att_m_fit = good_enough_distance(att_mom_goal, satellite['Metrics'][6])
        att_k_fit = good_enough_distance(att_know_goal, satellite['Metrics'][7])
        wave_fit = nearest_distance(wave_goal, satellite['Metrics'][8], 0.005)
        wave_d_fit = good_enough_distance(wave_det_goal, satellite['Metrics'][9])
        satellite['Fitness'] = np.array([vol_fit, mass_fit, cpu_fit, power_fit, br_d_fit, br_u_fit, att_m_fit,
                                         att_k_fit, wave_fit, wave_d_fit])

    # satellite['Metrics'] = np.array([volume_met, mass_met, cpu_met, power_met, br_down_met, br_up_met, att_met,
    #                                  att_know_met, wavelength_met, wave_det_met])
    return population


def nearest_distance(goal, metric, leeway):
    """
    This function calculates the distance for metrics that aim to be the closest to the desired requirement
    :param goal:
    :param metric:
    :param leeway: The amount of distance that a metric can be within a goal and be considered near enough to zero
    :return:
    """
    if np.abs(metric) < 10e-12:
        return 1
    else:
        return np.float64(np.abs(goal-metric) - leeway).clip(min=0, max=1)


def good_enough_distance(goal, metric):
    """
    This function calculates the distance for metrics that only need to reach a threshold. Anything above the goal is
    considered to be successful. Higher is better
    :param goal:
    :param metric:
    :return:
    """
    if metric > goal:
        return 0
    else:
        return np.float64(goal-metric).clip(min=0, max=1)