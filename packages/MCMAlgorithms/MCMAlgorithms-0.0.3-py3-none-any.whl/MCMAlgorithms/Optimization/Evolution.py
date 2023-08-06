import copy

import numpy as np
import pandas as pd


class Genetic:

    def __init__(self, max_iteration=50, chromosome_num=30, cross_prob=0.8, mutation_prob=0.0075, cross_point=1):
        """
        The Setting of Genetic Algorithm
        :param max_iteration: max iteration of genetic algorithm, with default as 50, positive int
        :param chromosome_num: the number of chromosome in the algorithm, with default as 30, positive odd greater than 1
        :param cross_prob: probability of crossing, with default as 0.8, float in [0, 1]
        :param mutation_prob: probability of mutation, with default as 0.0075, float in [0,1]
        :param cross_point: point of crossing, with default as 1, positive int
        """
        self.__max_iteration = int(max_iteration)
        self.__chroms = 2 if int(chromosome_num) < 2 else int(chromosome_num)
        if self.__chroms % 2:
            self.__chroms += 1
        self.__pc = 0.0 if cross_prob < 0 else (1.0 if cross_prob > 1 else cross_prob)
        self.__pm = 0.0 if mutation_prob < 0 else (1.0 if mutation_prob > 1 else mutation_prob)
        self.__cp = 1 if int(cross_point) < 1 else int(cross_point)
        np.random.seed(123456)

    def __mutation(self, solutions, mutation_fun=None):
        if mutation_fun is None:
            # Calculate the number of bits to mutate
            total_bits_number = solutions.shape[0] * solutions.shape[1]
            mutation_bits_number = int(total_bits_number * self.__pm)
            # Mutation
            bit_vector = solutions.reshape(1, -1).squeeze()
            idxs = np.arange(len(bit_vector))
            np.random.shuffle(idxs)
            select_bits_idx = idxs[:mutation_bits_number]
            bit_vector[select_bits_idx] = 1 - bit_vector[select_bits_idx]
            mutated_solutions = bit_vector.reshape(self.__chroms, -1)
        else:
            mutated_solutions = copy.deepcopy(solutions)
            for idx in range(self.__chroms):
                p = np.random.rand()
                if p < self.__pm:
                    mutated_solutions[idx, :] = mutation_fun(mutated_solutions[idx, :])
        return copy.deepcopy(mutated_solutions)

    def __init_mutation(self, initial_solution, mutation_fun=None):
        chromosomes = np.zeros((self.__chroms, len(initial_solution)))
        idxs = np.arange(len(initial_solution))
        for idx in range(self.__chroms):
            if mutation_fun is None:
                np.random.shuffle(idxs)
                select_bits_num = np.random.randint(len(initial_solution) + 1)
                select_bits_idxs = idxs[:select_bits_num]
                cp = copy.deepcopy(initial_solution)
                cp[select_bits_idxs] = 1 - cp[select_bits_idxs]
            else:
                cp = mutation_fun(initial_solution)
            chromosomes[idx, :] = cp
        return chromosomes

    def __cross(self, solution1, solution2):
        # The cut points
        idxs = np.arange(len(solution1))
        np.random.shuffle(idxs)
        point_exchanges = np.sort(np.hstack((idxs[:self.__cp], np.array([len(solution1)]))))
        # Crossing
        solution1 = copy.deepcopy(solution1)
        solution2 = copy.deepcopy(solution2)
        exchange_flag = 0
        for room_idx in range(self.__cp):
            if exchange_flag:
                point1 = point_exchanges[room_idx]
                point2 = point_exchanges[room_idx + 1]
                solution1[point1: point2], solution2[point1: point2] = solution2[point1: point2], solution1[point1: point2]
            exchange_flag = 1 - exchange_flag
        return solution1, solution2

    def __select(self, solutions, initial_shape, fitness_fun):
        # Structure Probability of selection
        fitness = np.zeros((1, self.__chroms)).squeeze()
        for idx in range(self.__chroms):
            solution = solutions[idx, :].reshape(initial_shape)
            fitness[idx] = fitness_fun(solution)
        best_fitness = np.min(fitness)
        best_chorm = solutions[np.argmin(fitness), :]
        fitness += (2 * np.min(fitness))  # avoid negative fitness
        prob = 1 - fitness / np.sum(fitness)
        cum_prob = np.cumsum(prob)
        # Selection
        new_solution = np.zeros_like(solutions)
        for idx in range(self.__chroms):
            p = np.random.rand()
            select_chrom_idx = np.argwhere(cum_prob >= p)[0, 0]
            new_solution[idx, :] = solutions[select_chrom_idx, :]
        return copy.deepcopy(new_solution), best_fitness, best_chorm

    def optimization(self, initial_solution, fitness_fun, legal_fun=None, mutation_fun=None):
        """
        Apply genetic algorithm for optimization
        :param initial_solution: list of numbers, 1-D ndarray or 1-D torch tensor
        :param fitness_fun: function of minimization, fitness_fun(solution) should return a float or int
        :param legal_fun: function of making the solution legal, legal_fun(solution) should return a solution
                          for mutation, please input mutation_fun, default as None (all solution is legal)
        :param mutation_fun: function of mutation without random seed setting, mutation_fun(solution) should
                          return a solution, default as None (apply tradition mutation method)
        :return: (optimized best solution, the best lost in each epoch in the optimization progress)
        """
        # Initialization
        initial_shape = initial_solution.shape
        chroms = self.__init_mutation(initial_solution, mutation_fun)
        if not (legal_fun is None):
            for idx in range(self.__chroms):
                chroms[idx, :] = legal_fun(chroms[idx, :])
        best_chrom = copy.deepcopy(initial_solution)
        best_loss = fitness_fun(best_chrom)
        for idx in range(self.__chroms):
            loss = fitness_fun(chroms[idx, :])
            if loss < best_loss:
                best_chrom = chroms[idx, :]
                best_loss = loss
        # Start iteration
        log_df = pd.DataFrame(dict.fromkeys(('Epoch', 'Best Loss'), []))
        for epoch in range(self.__max_iteration):
            # Selection
            chroms, epoch_best_fitness, epoch_best_chrom = self.__select(chroms, initial_shape, fitness_fun)
            if epoch_best_fitness < best_loss:
                best_loss = epoch_best_fitness
                best_chrom = epoch_best_chrom
            # Cross
            cross_chrom_num = int(self.__chroms * self.__pc)
            cross_chrom_num = cross_chrom_num + 1 if cross_chrom_num % 2 else cross_chrom_num
            cross_pair_num = cross_chrom_num // 2
            idxs = np.arange(self.__chroms)
            np.random.shuffle(idxs)
            for pair_idx in range(cross_pair_num):
                chrom1_idx = idxs[2 * pair_idx]
                chrom2_idx = idxs[2 * pair_idx + 1]
                chroms[chrom1_idx, :], chroms[chrom2_idx, :] = self.__cross(chroms[chrom1_idx, :], chroms[chrom2_idx, :])
            # Mutation
            chroms = self.__mutation(chroms, mutation_fun)
            if not (legal_fun is None):
                for idx in range(self.__chroms):
                    chroms[idx, :] = legal_fun(chroms[idx, :])
            log_df = log_df.append({'Epoch': epoch + 1, 'Best Loss': epoch_best_fitness}, ignore_index=True)
        return best_chrom, log_df
