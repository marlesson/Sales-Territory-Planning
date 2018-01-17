"""Genetic Algorithmn Implementation
see:
http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
"""

import argparse

# Genetic A
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticFunctions
from genetic_algorithm.sales_territories import SalesTerritories
from genetic_algorithm.chromo_summary import ChromoSummary
from models.salesman import *
from models.client import *
from util  import *

import yaml
from datetime import datetime

if __name__ == "__main__":

  # Get Run Params
  parser = argparse.ArgumentParser(description='Process some integers.')

  parser.add_argument('--input',    help='File with data', required=True)
  parser.add_argument('--priority', help='File with Priority matrix')
  parser.add_argument('--output',   help='Output Path', default='output/test')
  parser.add_argument('--params',   help='Configuration', default='conf.yml')

  parser.add_argument('--prob_mutation', type=float, default=0.2)
  parser.add_argument('--prob_crossover', type=float, default=0.9)
  parser.add_argument('--generations', type=int, default=100)
  parser.add_argument('--init_population', type=int, default=800)
  parser.add_argument('--elitism', type=int, default=1)
  parser.add_argument('--local_search', type=bool, default=False)

  parser.add_argument('--debug', type=int, default=0)
  parser.add_argument('--processes', type=int, default=4)

  
  args   = parser.parse_args()
  params = yaml.load(open(args.params))

  log(args)
  log(datetime.now())
  
  if not os.path.exists(args.output):
    os.makedirs(args.output)

  # Read Dataset
  if args.debug == 1:
    clients, clients_index, salesman, \
      salesman_index, initial_territory = read_dataset_test(args.input)
  else:
    clients, clients_index, salesman, \
      salesman_index, initial_territory = read_dataset(args.input)


  # Build distance matrix
  dist_matrix     = build_dist_matrix(clients, salesman)
  
  # Build priority Matrix
  priority_matrix = build_priority_matrix(args.priority, clients_index, salesman_index)
  
  if args.debug == 1 and not args.priority is None:
    priority_matrix = build_priority_matrix_test(clients, salesman, initial_territory)

  print(priority_matrix)
  
  # Genetic Algorithm with Configuration
  ga = GeneticAlgorithm(
        SalesTerritories(salesman, clients, 
          dist_matrix, priority_matrix, initial_territory, 
          limit=args.generations, 
          size=args.init_population,
          prob_crossover=args.prob_crossover,
          prob_mutation=args.prob_mutation,
          local_search=args.local_search,
          elitism=args.elitism,
          params=params)
        )

  log("Init Otimization...\n\n")

  population = ga.run(args.processes)

  # Best Solution
  best_territory = ga.best_solution
  log("Best Solution: "+str(ga.genetics.fitness(best_territory)))
  
  # History
  create_history_df(ga.avg_fitness).to_csv("{}/avg_fitness.csv".format(args.output))
  create_history_df(ga.best_fitness).to_csv("{}/best_fitness.csv".format(args.output))

  #for k in ga.genetics.fn.keys():
  #  create_history_df(ga.genetics.fn[k]).to_csv("{}/{}_fitness.csv".format(args.output, k))

  # Summary 
  chromo_summary  = ChromoSummary(salesman, clients, dist_matrix, priority_matrix)

  methods = [
    ['total_clients_per_salesman', chromo_summary.total_clients_per_salesman],
    ['benefit_per_salesman', chromo_summary.benefit_per_salesman],
    ['workload_per_salesman', chromo_summary.workload_per_salesman],
    ['dist_per_salesman', chromo_summary.dist_per_salesman],
    ['sustainability_per_salesman', chromo_summary.sustainability_per_salesman]
  ]

  for method in methods:
    name, method = method

    values_before = method(initial_territory)
    values_after  = method(best_territory)

    df_before = create_salesterritory_df(salesman_index, values_before)
    df_after  = create_salesterritory_df(salesman_index, values_after)

    df_before.to_csv("{}/original_{}.csv".format(args.output, name))
    df_after.to_csv("{}/optimized_{}.csv".format(args.output, name))

  # Save
  save_sales_territory(args.output, 
                        clients_index, salesman_index, 
                        initial_territory, best_territory)
  log(datetime.now())