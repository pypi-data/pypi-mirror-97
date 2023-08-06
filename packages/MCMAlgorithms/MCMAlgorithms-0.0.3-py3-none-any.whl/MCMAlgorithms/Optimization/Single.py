import copy

import numpy as np
import pandas as pd


class SimulateAnnealing:

    def __init__(self, T0=1000.0, Tend=1.0, mode='normal'):
        """
        The setting of Simulate Annealing Optimization Algorithm
        :param T0: The start temperature, with 1000.0 as default, positive float
        :param Tend: The end temperature, with 1.0 as default, postive float smaller than T0
        :param mode: Annealing mode, string in ('normal', 'fast')
        """
        self.__T0 = T0
        self.__Tend = Tend
        self.__mode = mode

    def optimize(self, initial_solution, fitness_fun):
        """
        Apply simulated annealing optimization
        :param initial_solution: list of numbers, 1-D ndarray or 1-D torch tensor
        :param fitness_fun: object function of minimization, fitness_fun(solution) should return a float or int
        :return: (optimized best solution, the log of loss in the optimization progress)
        log format: pandas dataframe, columns: Iteration, Old Loss, New Loss, accept probability, accept or not
        """
        # Initialization
        np.random.seed(123456)
        T = self.__T0
        old_solution = copy.deepcopy(initial_solution)
        old_fitness = fitness_fun(old_solution)
        best_solution = copy.deepcopy(initial_solution)
        best_loss = fitness_fun(best_solution)
        log_df = pd.DataFrame(dict.fromkeys(('Iteration', 'Old Loss', 'New Loss', 'p', 'Accept'), []))
        # Iteration
        iteration_idx = 0
        while T > self.__Tend:
            iteration_idx += 1
            # Evaluate the fitness function
            idx = np.arange(len(initial_solution))
            np.random.shuffle(idx)
            idx1, idx2 = idx[0], idx[1]
            new_solution = copy.deepcopy(old_solution)
            new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]
            new_fitness = fitness_fun(new_solution)
            # Decide whether to accept the new solution
            if new_fitness < old_fitness:
                old_solution = copy.deepcopy(new_solution)
                log_df = log_df.append({'Iteration': iteration_idx, 'Old Loss': old_fitness,
                                        'New Loss': new_fitness, 'p': 1.0, 'Accept': 'yes'},
                                       ignore_index=True)
                old_fitness = new_fitness
                if new_fitness < best_loss:
                    best_loss = new_fitness
                    best_solution = copy.deepcopy(new_solution)
            else:  # Metropolis principle
                accept_prob = np.exp(-(new_fitness - old_fitness) / T)
                p = np.random.random()
                if p <= accept_prob:
                    old_solution = copy.deepcopy(new_solution)
                    log_df = log_df.append({'Iteration': iteration_idx, 'Old Loss': old_fitness,
                                            'New Loss': new_fitness, 'p': p, 'Accept': 'yes'},
                                           ignore_index=True)
                    old_fitness = new_fitness
                else:
                    log_df = log_df.append({'Iteration': iteration_idx, 'Old Loss': old_fitness,
                                            'New Loss': new_fitness, 'p': p, 'Accept': 'no'},
                                           ignore_index=True)
            # Annealing
            if self.__mode == 'normal':
                T = self.__T0 / np.log1p(iteration_idx)
            else:
                T = self.__T0 / (iteration_idx + 1)
        return best_solution, log_df


class TabuSearch:

    def __init__(self, tabu_length=5, max_epoch=50):
        """
        The parameter of tabu search optimization algorithm
        :param tabu_length: the length of tabu list, with default as 5, positive int
        :param max_epoch: max iteration of tabu search algorithm, with default as 50, positive int
        """
        self.__tabu_len = int(tabu_length)
        self.__max_epoch = int(max_epoch)

    def optimize(self, initial_solution, fitness_fun):
        """
        Apply tabu search optimization
        :param initial_solution: list of numbers, 1-D ndarray or 1-D torch tensor
        :param fitness_fun: object function of minimization, fitness_fun(solution) should return a float or int
        :return: (optimized best solution, the loss in the optimization progress)
        """
        # Initialization
        tabu_list = -1 * np.ones((self.__tabu_len, 2))
        best_solution = copy.deepcopy(initial_solution)
        best_fitness = fitness_fun(best_solution)
        temp_solution = copy.deepcopy(initial_solution)
        exchange_df = pd.DataFrame(dict.fromkeys(('Exchange', 'Loss'), []))
        for idx1 in range(len(initial_solution)):
            for idx2 in range(idx1 + 1, len(initial_solution)):
                exchange_df = exchange_df.append({'Exchange': np.array([idx1, idx2]), 'Loss': np.inf},
                                                 ignore_index=True)
        log_df = pd.DataFrame(dict.fromkeys(('Epoch', 'Best Loss'), []))
        # Start iteration
        for epoch in range(self.__max_epoch):
            # Calculate the loss of possible shuffles and sort
            exchange_df['Loss'] = exchange_df['Exchange'].apply(lambda x: fitness_fun(self.__applyexchange(temp_solution,
                                                                                                           x)))
            exchange_df = exchange_df.sort_values('Loss')
            # Exam whether the first exchange get a better performance
            if exchange_df.iloc[0]['Loss'] < best_fitness:
                # Save the best result
                best_fitness = exchange_df.iloc[0]['Loss']
                epoch_fitness = exchange_df.iloc[0]['Loss']
                best_solution = self.__applyexchange(temp_solution, exchange_df.iloc[0]['Exchange'])
                temp_solution = copy.deepcopy(best_solution)
                # Add to tabu list
                tabu_list = np.vstack((exchange_df.iloc[0]['Exchange'], tabu_list[:-1, :]))
            else:
                # Verify each exchange until one is not in the tabu list
                idx = 0
                for search_idx in range(len(exchange_df)):
                    exchange = exchange_df.iloc[0]['Exchange']
                    minus = (tabu_list - exchange) == 0
                    if True in np.bitwise_and(minus[:, 0], minus[:, 1]):
                        idx += 1  # This exchange is in the tabu list
                    else:
                        break
                if idx == len(exchange_df):  # No exchange can be used, quit the algorithm
                    break
                # Take the temporal exchange
                epoch_fitness = exchange_df.iloc[idx]['Loss']
                temp_solution = self.__applyexchange(temp_solution, exchange_df.iloc[idx]['Exchange'])
                # Add to tabu list
                tabu_list = np.vstack((exchange_df.iloc[idx]['Exchange'], tabu_list[:-1, :]))
            log_df = log_df.append({'Epoch': epoch + 1, 'Best Loss': epoch_fitness}, ignore_index=True)
        # Return the result
        return best_solution, log_df

    def __applyexchange(self, solution, change_idxs):
        solution = copy.deepcopy(solution)
        solution[change_idxs[0]], solution[change_idxs[1]] = solution[change_idxs[1]], solution[change_idxs[0]]
        return solution
