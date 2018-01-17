"""Genetic Algorithmn Implementation
see:
http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
"""
import random
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool 
import multiprocessing
from tabu_search.tabu_search import TabuSearch
from tabu_search.sales_territories import SalesTerritories as TabuSalesTerritories


class GeneticAlgorithm(object):
    def __init__(self, genetics):
        self.genetics       = genetics
        self.best_solution  = None
        self.avg_fitness    = []
        self.best_fitness   = []
        pass

    def fitness(self, ch):
        return (self.genetics.fitness(ch),  ch)

    def run(self, processes=4):
        population = self.genetics.initial()
        pool       = multiprocessing.Pool(processes=processes)

        while True:
            fits_pops   = pool.map(self.fitness, population)

            pops_sorted = list(sorted(fits_pops, reverse=False))

            # Log
            self.avg_fitness.append(np.mean([f for f, ch in fits_pops]))
            self.best_fitness.append(pops_sorted[0][0])

            self.best_solution = pops_sorted[0][1].copy()

            # Test Break
            if self.genetics.check_stop(fits_pops): 
                break

            #in Local Search
            if self.genetics.local_search and self.genetics.counter % 50 == 0:
                fits_pops.extend(self.local_search(pool, self.best_solution.copy()))

            
            # New population
            population = self.next(fits_pops)

            # Elitism
            population[0] = self.best_solution

            pass
        return population

    def local_search(self, pool, ch):
        # Tabu Search
        tabu = TabuSearch(
            TabuSalesTerritories(self.genetics.salesman, self.genetics.clients, 
              self.genetics.dist_matrix, self.genetics.priority_matrix, ch, 
              limit=10, 
              tabu_size=100,
              params=self.genetics.params)
            )

        best_solution = tabu.run()

        neighbors     = tabu.problem.neighbors(best_solution[1])
        neighbors.append(best_solution[1])

        # Join
        fits_in_pops  = pool.map(self.fitness, neighbors)
        return fits_in_pops

    def next(self, fits):
        parents_generator = self.genetics.parents(fits)
        size  = self.genetics.size
        nexts = []
        while len(nexts) < size:
            parents  = next(parents_generator)
            cross    = random.random() < self.genetics.probability_crossover()
            children = self.genetics.crossover(parents) if cross else parents

            for ch in children:
                mutate = random.random() < self.genetics.probability_mutation()
                nexts.append(self.genetics.mutation(ch) if mutate else ch)
                pass
            pass
        return nexts[0:size]
    pass

class GeneticFunctions(object):
    def probability_crossover(self):
        r"""returns rate of occur crossover(0.0-1.0)"""
        return 1.0

    def probability_mutation(self):
        r"""returns rate of occur mutation(0.0-1.0)"""
        return 0.0

    def initial(self):
        r"""returns list of initial population
        """
        return []

    def fitness(self, chromosome):
        r"""returns domain fitness value of chromosome
        """
        return len(chromosome)

    def check_stop(self, fits_populations):
        r"""stop run if returns True
        - fits_populations: list of (fitness_value, chromosome)
        """
        return False

    def parents(self, fits_populations):
        r"""generator of selected parents
        """
        gen = iter(sorted(fits_populations))
        while True:
            f1, ch1 = next(gen)
            f2, ch2 = next(gen)
            yield (ch1, ch2)
            pass
        return

    def crossover(self, parents):
        r"""breed children
        """
        return parents

    def mutation(self, chromosome):
        r"""mutate chromosome
        """
        return chromosome
    pass
