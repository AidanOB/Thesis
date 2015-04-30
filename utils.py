__author__ = "Aidan O'Brien"

import matplotlib.pyplot as plt
import numpy as np

EXP_PATH = "G:\\Uni\\Dropbox\\Public\\Aidan\\Thesis\\Experiments\\"


def plot_ga_performance(performance, name):
    """
    This plots the performance metrics of a run of the genetic algorithm
    :param performance:
    :param name: The name of the experiment to go in when saving the plots automatically
    :return: Nothing
    """
    plt.figure(1)
    # plt.subplot(211)
    plt.plot(performance[:, 2])
    plt.title(name + 'Optimum Value')
    plt.xlabel('Generations')
    plt.ylabel('Minimum Distance per Generation')
    plt.figure(2)
    plt.plot(performance[:, 1])
    plt.title(name + 'Population Average Value')
    plt.xlabel('Generations')
    plt.ylabel('Minimum Distance per Generation')
    # plt.ion()
    plt.show()
    # plt.savefig("G:\\Uni\\Dropbox\\Public\\Aidan\\Thesis\\Experiments\\test.png", transparent=True)
    # return True


def save_pop_data(population, name, performance):
    """
    This function saves the population to disk
    :param population: The satellite population to be saved
    :param name: The name of the file to be saved as
    :return: Returns True
    """

    try:
        satellite_data_file = open(EXP_PATH + name + '.txt', 'w')
        print('Saving ' + name + ' to file')
        for satellite in population:
            satellite_data_file.write("%s\n\n" % satellite)
        satellite_data_file.close()

        print('Saving performance...')
        np.savetxt(EXP_PATH + name + '_performance.csv', performance, delimiter=',')
        # satellite_performance_file = open(exp_path + name + '_performance.txt')
        # satellite_performance_file.write("%s" % performance)
        # satellite_performance_file.close()
        print('Save complete')
        return True
    except:
        print('Unable to print ' + name + ' to file')
        return False


def load_exp_performance(name):
    """
    Loads the performance contained in name
    :param name: The name of the experiment
    :return: A numpy array containing the performance
    """
    return np.loadtxt(EXP_PATH + name + '_performance.csv', delimiter=',')


def sort_population(population):
    """
    This sorts the population in order of their rank, for ease of reading and evaluation
    :param population: list of satellites
    :return: sorted population
    """

    pop_size = len(population)
    sorted_pop = []
    i = 0

    while i < pop_size:
        for j in range(pop_size):
            if population[j]['Rank'] == i:
                sorted_pop.append(population[j])
                i += 1
                print('Placed in satellite: ' + str(i))
                continue

    return sorted_pop