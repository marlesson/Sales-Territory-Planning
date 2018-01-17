from genetic_algorithm.chromo_summary import ChromoSummary
from tabu_search.tabu_search import TabuSearch, TabuSearchFunctions

import random
import numpy as np


"""
example: Mapped guess prepared Text
"""
class SalesTerritories(TabuSearchFunctions):
    def __init__(self, salesman, clients, dist_matrix, priority_matrix, s0,
                 tabu_size=50, limit=1000,
                 params={}):

        self.salesman  = salesman
        self.clients   = clients
        self.dist_matrix     = dist_matrix
        self.priority_matrix = priority_matrix
        self.chromo_summary  = ChromoSummary(salesman, clients, dist_matrix, priority_matrix)

        self.s0        = s0

        self.counter   = 0

        self.tabu_list = []
        self.tabu_size = tabu_size
        self.limit     = limit

        self._max_sustentability = np.max(list(self.chromo_summary.sustainability_per_salesman(self.s0).values()))
        self._mean_workload      = np.mean(list(self.chromo_summary.workload_per_salesman(self.s0).values()))

        self.params = params

        print("Initial Solution: {}".format(self.fitness(self.s0)))
        pass

    def initial(self):
        return self.s0.copy()

    def fitness(self, chromo):
        f1 = f2 = 0
        len_salesman = self.chromo_summary._len_salesman

        #Balance Workload
        K    = self._mean_workload
        rep_workload  = self.chromo_summary.workload_per_salesman(chromo)
        f1   = np.sum([np.abs(rep_workload[i] - K) for i in range(len_salesman)])/(K*len_salesman)

        # Sustentabiliti
        L    = 50000 #self._max_sustentability
        sust = self.chromo_summary.sustainability_per_salesman(chromo, with_priority = True)
        f2   = np.sum([np.abs(sust[i] - L) for i in range(len_salesman)])/(L*len_salesman)

        # Dist
        dist  = self.chromo_summary.dist_per_salesman(chromo)
        f4    = np.sum([dist[i] for i in range(len_salesman)])/(self.chromo_summary.dist_max()*len_salesman)

        # Clientes
        cli   = self.chromo_summary.total_clients_per_salesman(chromo)

        # Faturamento
        fatu  = self.chromo_summary.benefit_per_salesman(chromo)

        # Apply Restrictions
        _r = self.restrictions(cli, fatu)

        return (f1*0.05 + f2*0.9 + f4*0.05)*_r
    
    def restrictions(self, cli, fatur):
        len_salesman = self.chromo_summary._len_salesman
        len_clients = self.chromo_summary._len_clients

        # Total CLients
        max_clients  = self.params['problem']['max_clients']
        min_clients  = self.params['problem']['min_clients']
        min_faturamento = self.params['problem']['min_faturamento']
        mean_clients = (max_clients-min_clients)/2

        cli_r   = 0
        fatur_r = 0
        for i in range(len_salesman):
            # Sustentability
            if fatur[i] <  min_faturamento:
                fatur_r = fatur_r + (min_faturamento - fatur[i])
            fatur_r = (fatur_r/((min_faturamento+1)*len_salesman))

            # Clients
            if cli[i] <  min_clients or cli[i] > max_clients:
                cli_r = cli_r + (np.abs(cli[i] - mean_clients))
            cli_r = (cli_r/len_salesman)
        
        cli_r   = (1+cli_r)
        fatur_r = (1+fatur_r)
        # Minimun sustentability

        return cli_r*0.5 + fatur_r*0.5

    def check_stop(self, fits_populations):
        self.counter += 1
        if self.counter % 10 == 0:
            fits  = [f for f, ch in fits_populations]
            best  = min(fits)
            worst = max(fits)
            ave   = sum(fits) / len(fits)
            print(
                "[I %3d] score=(%2f, %2f, %2f): %r" %
                (self.counter, best, ave, worst,
                 [len(fits_populations)]))
            pass

        return self.counter >= self.limit

    def neighbors(self, chromosome):
        neighbors = []

        for i in range(len(chromosome)):
            new_neighbors    = chromosome.copy()
            new_neighbors[i] = random.randint(0, self.chromo_summary._len_salesman-1)
            neighbors.append(new_neighbors)

        return neighbors  

    def is_tabu(self, chromosome):
        return chromosome in self.tabu_list

    def add_tabu_list(self, item):
        if len(self.tabu_list) >= self.tabu_size:
            self.tabu_list.pop(0)
        
        self.tabu_list.append(item)
    pass