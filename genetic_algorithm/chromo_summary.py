import random
import numpy as np

"""
example: Mapped guess prepared Text
"""
class ChromoSummary(object):
    def __init__(self, salesman, clients, dist_matrix, priority_matrix, cost_per_km = 1.78, max_clients=120):
        self.salesman  = salesman
        self.clients   = clients
        self.dist_matrix     = dist_matrix
        self.priority_matrix = priority_matrix   
        self.cost_per_km     = cost_per_km     
        self.max_clients     = max_clients

        self.init_const_values()
        
    def init_const_values(self):
        self._benefit_sum = None 
        self._dist_max    = None
        self._max_sustentability = None
        self._max_workload = None
        self._len_salesman = len(self.salesman)
        self._len_clients  = len(self.clients)

    def cost_benefit(self, chromo):
        benefit = {}
        cost    = {}

        for i in range(self._len_salesman):
            cost[i]    = 0
            benefit[i] = 0

        for client in range(self._len_clients):
            salesman       = chromo[client]
            
            cost[salesman]    = cost[salesman] + self.dist_matrix[salesman][client]
            benefit[salesman] = benefit[salesman] + self.clients[client].benefit

        list_cost    = list(cost.values())
        list_benefit = list(benefit.values())

        return np.sum(list_cost)/np.sum(list_benefit)

    def dist(self, chromo, with_priority = False):
        dist      = self.dist_per_salesman(chromo, with_priority)
        list_dist = list(dist.values())

        return np.sum(list_dist)

    def dist2cost(self, dist):
        return dist * self.cost_per_km

    def clients_per_salesman(self, chromo):
        clients = {}

        for i in range(self._len_salesman):
            clients[i] = []

        for client in range(self._len_clients):
            salesman          = chromo[client]
            clients[salesman].append(client)

        return clients

    def total_visits_clients_per_salesman(self, chromo):
        size = {}

        for i in range(self._len_salesman):
            size[i] = 0        

        for client_i in range(self._len_clients):
            salesman       = chromo[client_i]
            visits         = self.clients[client_i].visits

            size[salesman] = size[salesman] + visits

        return size

    def total_clients_per_salesman(self, chromo):
        size = {}

        for i in range(self._len_salesman):
            size[i] = 0        

        for client in range(self._len_clients):
            salesman       = chromo[client]
            size[salesman] = size[salesman] + 1

        return size

    def cost_per_salesman(self, chromo, with_priority = False):
        cost    = {}
        dist    = self.dist_per_salesman(chromo, with_priority)

        for i in range(self._len_salesman):
            cost[i] = self.dist2cost(dist[i])

        return cost


    def workload_per_salesman(self, chromo):
        workload = {}

        for i in range(self._len_salesman):
            workload[i] = 0

        for client in range(self._len_clients):
            salesman            = chromo[client]
            workload[salesman]  = workload[salesman] + self.clients[client].time_service * self.clients[client].visits

        return workload

    def max_workload(self):
        if self._max_workload == None:
            self._max_workload = 0
            for client in range(self._len_clients):
                self._max_workload  = self._max_workload + self.clients[client].time_service * self.clients[client].visits

            self._max_workload = self._max_workload/self._len_salesman

        return self._max_workload

    # Max distance
    def dist_max(self):
        if self._dist_max == None:
            dist = []

            for client in range(self._len_clients):
                for salesman in range(self._len_salesman):
                    value     = self.dist_matrix[salesman][client] * self.clients[client].visits
                    dist.append(value)

            self._dist_max = np.max(dist) 

        return self._dist_max


    # All Distance per salesman
    #
    def dist_min_max_per_salesman(self, chromo, with_priority = False):
        dist_max = {}
        dist_min = {}
        dist     = {}

        for i in range(self._len_salesman):
            dist_max[i] = []
            dist_min[i] = []
            dist[i]     = []

        for client in range(self._len_clients):
            salesman  = chromo[client]
            value     = self.dist_matrix[salesman][client] * self.clients[client].visits
            dist[salesman].append(value)

        # max
        for i in range(self._len_salesman):
            if len(dist[i]) > 0:
                dist_max[i] = np.max(dist[i])
                dist_min[i] = np.min(dist[i])
            else:
                dist_max[i] = 0
                dist_min[i] = 0
        return [dist_max, dist_min, len(dist[i])]


    # All Distance per salesman
    #
    def dist_per_salesman(self, chromo, with_priority = False):
        dist = {}

        for i in range(self._len_salesman):
            dist[i] = []

        for client in range(self._len_clients):
            salesman      = chromo[client]

            value     = self.dist_matrix[salesman][client] * self.clients[client].visits

            dist[salesman].append(value)

        # sum
        for i in range(self._len_salesman):
           dist[i] = np.sum(dist[i])

        return dist


    def dist_benefit_per_salesman(self, chromo, with_priority = False):
        dist_benefit = {}
        cost    = self.dist_per_salesman(chromo)
        benefit = self.benefit_per_salesman(chromo, with_priority)

        for i in range(self._len_salesman):
            if benefit[i] == 0 or cost[i] == 0:
                dist_benefit[i] = 1
            else:
                dist_benefit[i] = cost[i]/benefit[i]

        return dist_benefit


    def benefit_per_salesman(self, chromo, with_priority = False):
        benefit = {}

        for i in range(self._len_salesman):
            benefit[i] = 0

        for client in range(self._len_clients):
            salesman  = chromo[client]
            
            if with_priority:
                value     = (self.clients[client].benefit * self.priority_matrix[salesman][client])
            else:
                value     = (self.clients[client].benefit)

            benefit[salesman]   = benefit[salesman] + value

        return benefit

    def sustainability_per_salesman(self, chromo, with_priority = False):
        sust    = {}
        cost    = self.cost_per_salesman(chromo)
        benefit = self.benefit_per_salesman(chromo, with_priority)

        for i in range(self._len_salesman):
            sust[i] = (benefit[i] - cost[i])

        return sust

    def priority_evaluation(self, chromo):
        pri = []

        for client in range(self._len_clients):
            salesman       = chromo[client]
            pri.append(self.priority_matrix[salesman][client])

        return np.sum(pri)

    def diff(self, chromo1, chromo2):
        diff = []

        for i in range(len(self.clients)):
            diff.append(chromo1[i] != chromo2[i])

        return diff