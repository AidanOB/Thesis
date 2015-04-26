__author__ = "Aidan O'Brien"

import matplotlib.pyplot as plt


def plot_ga_performance(performance, name):
    """
    This plots the performance metrics of a run of the genetic algorithm
    :param performance:
    :param name: The name of the experiment to go in when saving the plots automatically
    :return: Nothing
    """
    plt.figure(1)
    plt.subplot(211)
    plt.plot(performance[:, 2])
    plt.title('Optimum Value')
    plt.xlabel('Generations')
    plt.ylabel('Minimum Distance per Generation')
    plt.figure(212)
    plt.plot(performance[:, 1])
    plt.title('Population Average Value')
    plt.xlabel('Generations')
    plt.ylabel('Minimum Distance per Generation')
    plt.show()
    plt.savefig('test.png')