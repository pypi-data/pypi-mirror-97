import copy

import numpy as np
import pandas as pd


class PSO:

    def __init__(self, max_iteration=50, swarm_num=20, c1=2, c2=2, w_ini=0.9, w_end=0.4):
        """
        The setting of PSO algorithm
        :param max_iteration: max iteration of PSO algorithm, with default as 50, positive int
        :param swarm_num: the number of swarm, with default as 20, int
        :param c1: learning coefficient, with default as 2, positive float
        :param c2: learning coefficient, with default as 2, positive float
        :param w_ini: initial origin velocity weight, with default as 0.9, positive float
        :param w_end: ending origin velocity weight, with default as 0.4, positive float smaller than w_ini
        """
        self.__c1 = c1
        self.__c2 = c2
        self.__w_ini = w_ini
        self.__w_end = w_end
        self.__max_iteration = int(max_iteration)
        self.__swarm_num = int(swarm_num)
        np.random.seed(123456)

    def optimize(self, initial_solution, fitness_fun, solution_lower_bound=None, solution_upper_bound=None):
        """
        Apply PSO optimization
        :param initial_solution: list of numbers, 1-D ndarray or 1-D torch tensor
        :param fitness_fun: object function of minimization, fitness_fun(solution) should return a float or int
        :param solution_lower_bound: list of numbers, 1-D ndarray or 1-D torch tensor
        :param solution_upper_bound: list of numbers, 1-D ndarray or 1-D torch tensor
        :return: (optimized best solution, the best lost in each epoch in the optimization progress)
        """
        # Initialization
        initial_solution = copy.deepcopy(initial_solution)
        initial_shape = initial_solution.shape
        if solution_lower_bound is None:
            lower_bound = None
        else:
            lower_bound = np.array(solution_lower_bound).reshape(1, -1)
        if solution_upper_bound is None:
            upper_bound = None
        else:
            upper_bound = np.array(solution_upper_bound).reshape(1, -1)
        all_solutions = np.random.randn(self.__swarm_num, len(initial_solution))
        if not (lower_bound is None):
            for idx in range(self.__swarm_num):
                all_solutions[idx, :] = np.max(np.vstack((all_solutions[idx, :], lower_bound)), 0).reshape(1, -1)
        if not (upper_bound is None):
            for idx in range(self.__swarm_num):
                all_solutions[idx, :] = np.min(np.vstack((all_solutions[idx, :], upper_bound)), 0).reshape(1, -1)
        all_best_solutions = copy.deepcopy(all_solutions)
        all_fitness = np.array([np.inf] * self.__swarm_num)
        for idx in range(self.__swarm_num):
            solution = all_solutions[idx, :].reshape(initial_shape)
            all_fitness[idx] = fitness_fun(solution)
        best_idx = np.argmin(all_fitness)
        best_solution = all_solutions[best_idx, :].reshape(initial_shape)
        best_fitness = all_fitness[best_idx]
        velocity = np.random.random(all_solutions.shape)
        # Optimization
        log_df = pd.DataFrame(dict.fromkeys(('Epoch', 'Best Loss'), []))
        for epoch in range(self.__max_iteration):
            # Update Velocity and Solution
            w = (self.__w_ini - self.__w_end) * (self.__max_iteration - epoch) / self.__max_iteration + self.__w_end
            velocity = w * velocity + self.__c1 * np.random.random(velocity.shape) * (all_best_solutions - all_solutions) + self.__c2 * np.random.random(velocity.shape) * (best_solution - all_solutions)
            all_solutions += velocity
            # Limit the solution
            if not (lower_bound is None):
                for idx in range(self.__swarm_num):
                    all_solutions[idx, :] = np.max(np.vstack((all_solutions[idx, :], lower_bound)), 0).reshape(initial_shape)
            if not (upper_bound is None):
                for idx in range(self.__swarm_num):
                    all_solutions[idx, :] = np.min(np.vstack((all_solutions[idx, :], upper_bound)), 0).reshape(initial_shape)
            # Calculate fitness
            for idx in range(self.__swarm_num):
                solution = all_solutions[idx, :].reshape(initial_shape)
                all_fitness[idx] = fitness_fun(solution)
            # Get the best fitness and compare
            epoch_best_idx = np.argmin(all_fitness)
            epoch_best_fitness = all_fitness[epoch_best_idx]
            if epoch_best_fitness < best_fitness:
                best_fitness = epoch_best_fitness
                best_solution = copy.deepcopy(all_solutions[epoch_best_idx, :]).reshape(initial_shape)
            log_df = log_df.append({'Epoch': epoch, 'Best Loss': best_fitness}, ignore_index=True)
        return best_solution, log_df


class Bird(PSO):

    def __init__(self, max_iteration=50, swarm_num=20, c1=2, c2=2, w_ini=0.9, w_end=0.4):
        super(Bird, self).__init__(max_iteration, swarm_num, c1, c2, w_ini, w_end, )
