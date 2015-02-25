__author__ = "Aidan O'Brien"

"""
A module which converts the csv files into pandas data frames, for easy retrieval.
"""

import pandas as pd
import numpy as np
from fuzzy_values import create_value_array

structures = pd.DataFrame.from_csv(path='./Component Files/structures.csv', sep=';', encoding='iso-8859-1')

components = pd.DataFrame.from_csv(path='./Component Files/components.csv', sep=';', encoding='iso-8859-1')

systems = pd.DataFrame.from_csv(path='./Component Files/systems.csv', sep=';', encoding='iso-8859-1')

comp_hidden = pd.DataFrame.from_csv(path='./Component Files/components_hidden.csv', sep=';', encoding='iso-8859-1')

comp_pre_built = pd.concat([comp_hidden, components], ignore_index=True)


def create_system_metrics(system):
    """
    This function takes a fully parsed system of raw data values and calculates the system's metric scores.
    :param system: A numpy array representing the system
    :return: A numpy array that contains metrics formulated for both the FAM algorithm and the genetic algorithm
    """
    pass


def calculate_cpu_metric(data, code, ram):
    """
    This function calculates the cpu's data and general capability based upon the memory and RAM available to it. It
    doesn't consider the speed of the chip. It calculates based on the following equation:
    metric = (data/max_data + code/max_code + ram/max_ram) / 3
    This normalises each value against the maximum value in the database. Then all are weighted equally
    Then the total is normalised into the range [0, 1]
    :param data: The dedicated data storage for the system
    :param code: The memory available to code or additional storage space
    :param ram: The memory in ram, important for more complicated processes onboard the satellite
    :return: A numerical value that contains the the calculated metric for the system
    """
    max_data = 15000  # Matching an ideal state
    max_code = 100  # Near enough to the maximum value to be an ideal state
    max_ram = 128  # Less than the maximum, but reaches an ideal state

    data_met = (data / max_data).clip(min=0, max=1)
    code_met = (code / max_code).clip(min=0, max=1)
    ram_met = (ram / max_ram).clip(min=0, max=1)

    return np.abs((data_met + code_met + ram_met) / 3).clip(min=0, max=1)


def calculate_br_down_metric(br_down):
    """
    This function calculates the down bit rate with a maximum of 100,000 kbps.
    :param br_down: A numerical value for the bit rate in kbps
    :return: A normalised value in the range [0, 1]
    """
    br_max = 100000
    return np.abs(br_down / br_max).clip(min=0, max=1)


def calculate_br_up_metric(br_up):
    """
    This function calculates the up bit rate with a maximum of 10,000 kbps, slightly above the maximum in the data set
    :param br_up: A numerical value for the bit rate in kbps
    :return: A normalised value in the range [0, 1]
    """
    br_max = 10000
    return np.abs(br_up / br_max).clip(min=0, max=1)


def calculate_attitude_metric(moment, mass, knowledge, axis):
    """
    This function calculates the moment compared to the total mass of the satellite. This is worth 40% of the metric,
    with the attitude determination being utilised for another 40% of the metric. The number of axis that can be
    controlled accounts for the final 20% of the metric
    :param moment:
    :param mass:
    :param knowledge:
    :param axis:
    :return:
    """


def create_system(sys_structure):
    """
    This function creates a system from the dict structure given. It combines the components listed and then returns
      the product specifications.
    :param sys_structure: A dict that lists all the components that are a part of the system
    :return: A dictionary the lists the product specifications as generated
    """
    pass


def parse_system(system, comps):
    """
    This function parses the data frame row for an individual system, converting it into a dictionary for creating the
     product specifications
    :param system: A row from a Pandas Data Frame.
    :param comps: Defines which components database to search
    :return: Two arrays, the first are the customer requirements features returned as fuzzy logic values, the second is
    the product specification values. These will not be normalised.
    """

    # Load the structure from the data frame given
    # print(system)
    struct = structures.loc[structures['Name'].isin([system['Structure']])]
    internal_slots = struct['Internal Slots'].values
    external_slots = struct['External Slots'].values
    internal_vol = struct.X[0] * struct.Y[0] * struct.Z[0]
    total_vol = 0

    # Extract the fuzzy values for the system and place them into a numpy array of features for FAM algorithm
    cust_reqs = create_value_array(system['Size'], system['Size Imp'], system['Mass Imp'], system['Down Sp'],
                                   system['Up Sp'], system['Alt Req'], system['Att Ctrl'], system['Remote'],
                                   system['RS Wave'], system['RS Accuracy'])

    comp_totals = system.to_dict()
    comp_list = list()
    ext_list = list()
    for heading in comp_totals:
        if "Comp" in heading:
            comp_list.append(heading)
        elif "Ext" in heading:
            ext_list.append(heading)

    parts_sum_matrix = np.zeros((0, 0))
    parts_max_matrix = np.zeros((0, 0))
    metric_matrix = np.zeros((0, 0))
    metric_min_matrix = np.zeros((0, 0))
    metric_max_matrix = np.zeros((0, 0))

    # This is horrible, work on making it better once it's proved to get the right outputs

    for part in comp_list:
        idx = comps['Name'] == system[part]
        metrics_sums, metrics_mins, metrics_max, sum_vals, max_vals = parse_component(comps.loc[idx])

        if parts_sum_matrix.shape == (0, 0):
            parts_sum_matrix = sum_vals
        else:
            parts_sum_matrix = np.concatenate((parts_sum_matrix, sum_vals), 1)
        if parts_max_matrix.shape == (0, 0):
            parts_max_matrix = max_vals
        else:
            parts_max_matrix = np.concatenate((parts_max_matrix, max_vals), 1)
        if metric_matrix.shape == (0, 0):
            metric_matrix = metrics_sums
        else:
            metric_matrix = np.concatenate((metric_matrix, metrics_sums), 1)
        if metric_min_matrix.shape == (0, 0):
            metric_min_matrix = metrics_mins
        else:
            metric_min_matrix = np.concatenate((metric_min_matrix, metrics_mins), 1)
        if metric_max_matrix.shape == (0, 0):
            metric_max_matrix = metrics_max
        else:
            metric_max_matrix = np.concatenate((metric_max_matrix, metrics_max), 1)

    for part in ext_list:
        idx = comps['Name'] == system[part]
        metrics_sums, metrics_mins, metrics_max, sum_vals, max_vals = parse_component(comps.loc[idx])
        print(part)
        cube_size = 1
        if part == "Ext Sides":
            metrics_sums = (4 * cube_size) * metrics_sums

        if parts_sum_matrix.shape == (0, 0):
            parts_sum_matrix = sum_vals
        else:
            parts_sum_matrix = np.concatenate((parts_sum_matrix, sum_vals), 1)
        if parts_max_matrix.shape == (0, 0):
            parts_max_matrix = max_vals
        else:
            parts_max_matrix = np.concatenate((parts_max_matrix, max_vals), 1)
        if metric_matrix.shape == (0, 0):
            metric_matrix = metrics_sums
        else:
            metric_matrix = np.concatenate((metric_matrix, metrics_sums), 1)
        if metric_min_matrix.shape == (0, 0):
            metric_min_matrix = metrics_mins
        else:
            metric_min_matrix = np.concatenate((metric_min_matrix, metrics_mins), 1)
        if metric_max_matrix.shape == (0, 0):
            metric_max_matrix = metrics_max
        else:
            metric_max_matrix = np.concatenate((metric_max_matrix, metrics_max), 1)


    parts_sum_matrix = parts_sum_matrix.astype(np.float)
    parts_max_matrix = parts_max_matrix.astype(np.float)
    # print(metric_matrix)
    print(metric_matrix.sum(axis=1))
    metric_min_matrix[metric_min_matrix == 0] = None
    metric_min_matrix = metric_min_matrix[~np.isnan(metric_min_matrix)]
    print(metric_min_matrix.min())
    print(metric_max_matrix.max(axis=1))
    # print(parts_sum_matrix.sum(axis=1))

    # print(parts_max_matrix.shape)
    # Todo calculate all components in the system and provide system outputs that can be converted into metrics
    metrics = np.concatenate((metric_matrix.sum(axis=1), np.array([metric_min_matrix.min()]),
                              metric_max_matrix.max(axis=1)), 0)

    cpu_met = calculate_cpu_metric(metrics[4], metrics[5], metrics[6])
    print(cpu_met)


def parse_component(component):
    """
    This function calculates the various dimensions and metrics that can be utilised for the features, then returns them
    for summation in the parse system function
    :param component: The single line dataframe or series to be parsed
    :return:
    """
    # Volume of the component in m^3
    volume = (component.X * component.Y * component.Z).values[0]

    # How many slots the component takes up
    internal_slots = component['Internal Slots'].values[0]

    if not component['External Slots'].values == 0:
        external = True
        external_slots = component['External Slots'].values[0]
    else:
        external = False
        external_slots = 0

    min_temp = component['Min Temp'].values[0]
    max_temp = component['Max Temp'].values[0]

    mass = component['Mass'].values[0]
    max_voltage = component['Voltage'].values[0]
    nom_power = component['Nom Power'].values[0]
    max_power = component['Power (W)'].values[0] - nom_power  # This returns the difference when activated
    discharge_time = component['Discharge Time (Wh)'].values[0]
    pixel_resolution = component['Resolution (MP)'].values[0]
    wavelength_resolution = component['Resolution(nm)'].values[0]
    min_wavelength = component['Min Wavelength (nm)'].values[0]
    max_wavelength = component['Max Wavelength (nm)'].values[0]
    field_of_view = component['Field of View (deg)'].values[0]
    rx_min = component['Receiver Min (MHz)'].values[0]
    rx_max = component['Receiver Max'].values[0]
    tx_min = component['Transmitter Min'].values[0]
    tx_max = component['Transmitter Max'].values[0]
    duplex = component['Duplex'].values[0] + 1
    br_down = component['Bit Rate Down'].values[0]
    br_up = component['Bit Rate Up'].values[0]
    data = component['Data Storage (MB)'].values[0]
    code = component['Code Storage (MB)'].values[0]
    ram = component['RAM'].values[0]
    att_know = component['Attitude Know (deg)'].values[0]
    att_view = component['Attitude View'].values[0]
    att_mom = component['Attitude Control moment'].values[0]
    max_prop = component['Max Propulsion (mN)'].values[0]
    att_type = component['Attitude Type'].values[0]
    axis = component['Axis control'].values[0]
    ctrl_area = component['Control Area (m^2)'].values[0]
    disposal = component['Disposal time(km/day)'].values[0]
    int_comms = component['Internal Comms'].values[0]
    comm_conn = component['IntCommConn'].values[0]
    price = component['Price ($US)'].values[0]

    metric_sums = np.array([[mass, duplex, br_down, br_up, data, code, ram, att_view, att_mom, max_prop, axis,
                               ctrl_area, disposal, price, pixel_resolution, wavelength_resolution, min_wavelength,
                               max_wavelength]]).T.astype(np.float)
    metric_mins = np.array([[att_know]]).T.astype(np.float)
    metric_maxs = np.array([[]]).T.astype(np.float)

    summation_values = np.array([[volume, mass, internal_slots, external_slots, nom_power, discharge_time, duplex,
                                 br_down, br_up, data, code, ram, att_know, att_view, att_mom, max_prop, att_type,
                                axis, ctrl_area, disposal, price]]).T
    min_max_values = np.array([[max_voltage, max_power, pixel_resolution, wavelength_resolution, min_temp, max_temp,
                               min_wavelength, max_wavelength, field_of_view, rx_min, rx_max, tx_min, tx_max]]).T

    #Todo, figure out a way to deal with the comms issue. possibly a later problem

    # print(summation_values)

    # Todo create matrix from arrays then sum each feature on the correct axis
    # Todo This will create the correct feature set
    # Other features will be made from summation of available slots/connects vs used
    return metric_sums, metric_mins, metric_maxs, summation_values, min_max_values