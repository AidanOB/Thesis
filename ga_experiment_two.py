__author__ = "Aidan O'Brien"


from nsga import *
import time
import utils

if __name__ == "__main__":
    targets = np.array([[0.5, 0.5, 0.265, 0.667, 0.5],
                        [0.667, 0.167, 0.265, 0.667, 0.5],
                        [0.5, 0.5, 0.265, 0.87, 0.5],
                        [0.667, 0.167, 0.265, 0.87, 0.5]])

    tests = targets.shape[0]

    for i in range(tests):
        print(targets[i, :])
        t = time.time()
        final_pop, perf, mets_perf = genetic_algorithm(100, 100, 0.3, targets[i, :])
        elapsed_time = time.time() - t
        print('Elapsed Time: ' + str(elapsed_time) + 's')
        utils.save_pop_data(final_pop, '\\experiment_two\\test' + str(i), perf, mets_perf)
        final_pop = utils.sort_population(final_pop)
        utils.save_pop_data(final_pop, '\\experiment_two\\test_sorted_' + str(i), perf, mets_perf)
        # performance = utils.load_exp_performance('\\experiment_one\\test' + str(i))