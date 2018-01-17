from genetic_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticFunctions
from genetic_algorithm.chromo_summary import ChromoSummary

import random
import numpy as np


"""
example: Mapped guess prepared Text
"""
class SalesTerritories(GeneticFunctions):
    def __init__(self, salesman, clients, dist_matrix, priority_matrix, s0,
                 limit=200, size=400,
                 prob_crossover=0.9, 
                 prob_mutation=0.2,
                 elitism=1,
                 local_search =False,
                 params={}):
        self.salesman  = salesman
        self.clients   = clients
        self.dist_matrix     = dist_matrix
        self.priority_matrix = priority_matrix
        self.chromo_summary  = ChromoSummary(salesman, clients, dist_matrix, priority_matrix)

        self.s0        = s0

        self.counter   = 0
        self.local_search = local_search
        
        self.limit = limit
        self.size  = size
        self.prob_crossover = prob_crossover
        self.prob_mutation  = prob_mutation
        self.elitism = elitism

        self._max_sustentability = np.max(list(self.chromo_summary.sustainability_per_salesman(self.s0).values()))
        self._mean_workload      = np.mean(list(self.chromo_summary.workload_per_salesman(self.s0).values()))

        self.params = params

        print("Initial Solution: {}".format(self.fitness(self.s0)))
        pass

    # GeneticFunctions interface impls
    def probability_crossover(self):
        return self.prob_crossover

    def probability_mutation(self):
        return self.prob_mutation

    # Initial population based in s0
    def initial(self):
        n = int(self.size*0.8)
        
        # Random
        population = [self.random_chromo() for j in range(self.size-n)]

        # Inicial Solution
        population.append(self.s0.copy())

        # Mutation of Initial Solution
        for i in range(n-1):
            population.append(self.mutation(self.s0.copy()))
        
        return population

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
            fatur_r = (fatur_r/(min_faturamento+1*len_salesman))

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
                "[G %3d] score=(%2f, %2f, %2f): %r" %
                (self.counter, best, ave, worst,
                 [len(fits_populations)]))
            pass

        return self.counter >= self.limit

    def parents(self, fits_populations):
        while True:
            father = self.tournament(fits_populations)
            mother = self.tournament(fits_populations)
            yield (father, mother)
            pass
        pass

    def crossover(self, parents):
        father, mother = parents
        index1 = random.randint(1, len(father) - 2)
        index2 = random.randint(1, len(father) - 2)
        if index1 > index2: index1, index2 = index2, index1
        child1 = father[:index1] + mother[index1:index2] + father[index2:]
        child2 = mother[:index1] + father[index1:index2] + mother[index2:]
        return (child1, child2)

    def mutation(self, chromosome):
        mutated = chromosome
        
        i           = random.randint(0, len(self.clients) -1)
        salesman_id = random.randint(0, len(self.salesman)-1)

        mutated[i]  = salesman_id

        for i in range(len(mutated)):
            if random.random() < 0.1:
                mutated[i] = random.randint(0, len(self.salesman)-1)

        return mutated

    def tournament(self, fits_populations):
        alicef, alice = self.select_random(fits_populations)
        bobf, bob = self.select_random(fits_populations)
        return alice if alicef < bobf else bob

    def select_random(self, fits_populations):
        return fits_populations[random.randint(0, len(fits_populations)-1)]

    def random_chromo(self):
        chromo = []
        
        for i in range(len(self.clients)):
            salesman_id = random.randint(0, len(self.salesman)-1)
            chromo.append(salesman_id)

        return chromo
    pass