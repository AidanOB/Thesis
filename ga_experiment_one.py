__author__ = "Aidan O'Brien"


from nsga import *
import time
import utils

if __name__ == "__main__":
    targets = np.array([[0.334, 0.167, 0.2667, 0.167, 0.5],
                        [0.334, 0.167, 0.5, 0.167, 0.5],
                        [0.334, 0.167, 0.334, 0.167, 0.5],
                        [0.334, 0.167, 0.2667, 10e-11, 0.5],
                        [0.334, 0.167, 0.5, 10e-11, 0.5],
                        [0.334, 0.167, 0.334, 10e-11, 0.5]])

    tests = targets.shape[0]

    for i in range(tests):
        print(targets[i, :])
        t = time.time()
        final_pop, perf = genetic_algorithm(100, 100, 0.3, targets[i, :])
        elapsed_time = time.time() - t
        print('Elapsed Time: ' + str(elapsed_time) + 's')
        utils.save_pop_data(final_pop, '\\experiment_one\\test' + str(i), perf)
        final_pop = utils.sort_population(final_pop)
        utils.save_pop_data(final_pop, '\\experiment_one\\test_sorted_' + str(i), perf)
        # performance = utils.load_exp_performance('\\experiment_one\\test' + str(i))