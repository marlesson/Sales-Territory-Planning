"""Tabu Search
see:
"""
import random
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool 
import multiprocessing


class TabuSearch(object):
    def __init__(self, problem):
        self.problem        = problem
        self.best_solution  = None
        self.avg_fitness    = []
        self.best_fitness   = []
        pass

    def fitness(self, ch):
        return (self.problem.fitness(ch),  ch)

    def run(self, processes=4):
        self.best_solution = self.fitness(self.problem.initial().copy())
        solution           = self.fitness(self.problem.initial().copy())

        #self.problem.add_tabu_list()
        pool      = multiprocessing.Pool(processes=processes)

        while True:
            neighbors   = self.problem.neighbors(solution[1])
            fits_pops   = pool.map(self.fitness, neighbors)

            # Busca melhor vizinho
            solution    = fits_pops[0]
            i           = 0
            i_tabu      = 0
            for f, ch in fits_pops:
                if not self.problem.is_tabu(i) and (f < solution[0]):
                    solution = (f, ch)
                    i_tabu   = i

                i = i + 1


            # Update Tabu
            self.problem.add_tabu_list(i_tabu)

            self.avg_fitness.append(np.mean([f for f, ch in fits_pops]))
            self.best_fitness.append(self.best_solution[0])

            # Update best solution
            if solution[0] < self.best_solution[0]:
              self.best_solution = solution
            
            # Test Break
            if self.problem.check_stop(fits_pops): 
                break

            pass
        return self.best_solution
    pass

class TabuSearchFunctions(object):
    def initial(self):
        r"""returns list of initial population
        """
        return None

    def fitness(self, chromosome):
        r"""returns domain fitness value of chromosome
        """
        return len(chromosome)

    def check_stop(self, fits_populations):
        r"""stop run if returns True
        - fits_populations: list of (fitness_value, chromosome)
        """
        return False

    def neighbors(self, chromosome):
        return []
    

    def add_tabu_list(self, item):
        pass
    pass
