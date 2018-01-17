"""Genetic Algorithmn Implementation
see:
"""

import numpy as np
import pandas as pd
import os
import random
import math
from models.client   import *
from models.salesman import *
from geopy.distance import vincenty


def filter_sample(df, size, seed = 42):
  return df.sample(size,random_state=seed)

#
# client_id, salesman_id, client_revenue_avg, client_lat,
# client_lon, salesman_lon, salesman_lat, salesman_cost
def read_dataset(file):
  clients  = []
  salesman = []
  sales_territory = []
  salesman_index  = []
  clients_index   = []

  df = pd.read_csv(file)

  #df = filter_sample(df, 200)

  # Read data
  log("Read Datasets... "+str(len(df)))

  # Salesman
  df_s = df[['salesman_id', 'salesman_lon', 
    'salesman_lat', 'salesman_cost']].drop_duplicates()
  df_s.set_index('salesman_id')

  for i, row in df_s.iterrows():
    salesman_index.append(row.salesman_id)
    salesman.append(Salesman(row.salesman_cost, 
      row.salesman_lat, row.salesman_lon))

  # Clients
  for i, row in df.iterrows():
    benefit = row.client_revenue_avg
    cli     = Client(benefit, row.client_lat, row.client_lon)

    if 'visit_in_month' in row:
      cli.visits =  row.visit_in_month
    
    if 'time_to_attend' in row:
      cli.time_service =  row.time_to_attend  

    cli.salesman_id = salesman_index.index(row.salesman_id)
    
    clients.append(cli)
    clients_index.append(row.client_id)

    # SalesTerritory
    sales_territory.append(int(cli.salesman_id))

  #random.seed(42)
  #random.shuffle(sales_territory)
  
  return [clients, clients_index, salesman, salesman_index, sales_territory]

def read_dataset_test(file=None):
  clients  = []
  salesman = []
  sales_territory = []
  salesman_index  = []
  clients_index   = []

  # Read data
  print("Read datasets...")

  # Salesman
  df_s  = pd.read_csv("./input/test/salesman.csv")
  for i, row in df_s.iterrows():
    salesman_index.append(i)
    salesman.append(Salesman(row.value, row.x, row.y))


  df_c  = pd.read_csv("./input/test/clients.csv")
  for i, row in df_c.iterrows():
    # Clients
    
    benefit = row.benefit

    cli = Client(benefit, row.client_lat, row.client_lon)

    cli.salesman_id = salesman_index.index(row.salesman_id)

    clients.append(cli)
    clients_index.append(i)

    sales_territory.append(int(cli.salesman_id))

  random.seed(42)
  random.shuffle(sales_territory)

  return [clients, clients_index, salesman, salesman_index, sales_territory]


# Distância em linha reta entra o ponto A e o ponto B
def dist(lat1, long1, lat2, long2):
    return vincenty((lat1, long1), (lat2, long2)).km


# Build matrix distance with km betwen clientsxsalesman
#
def build_dist_matrix(territory, salesman):
    log("Build Distance Matrix...")
    # Matrix
    m = np.zeros((len(salesman), len(territory)))

    # Rep
    for s in range(len(salesman)):
        # Cli
        for t in range(len(territory)):
            m[s, t] = dist(salesman[s].lat, salesman[s].lon, territory[t].lat, territory[t].lon)
    
    return m

# Build or Read priority matrix 
#
def build_priority_matrix(file, clients_index, salesman_index,  default_priority = 1):
    log("Build Priority Matrix...")
    # Matrix
    m = np.zeros((len(salesman_index), len(clients_index)))

    # Read dataset
    if file != None:
      df = pd.read_csv(file)
      df = df.set_index(['client_id', 'salesman_id'])

    # Rep
    for s in range(len(salesman_index)):
        # Cli
        for t in range(len(clients_index)):
            
            try:
              pry = df.loc[(int(clients_index[t]), int(salesman_index[s]))].priority
            except: 
              pry = default_priority

            m[s, t] = pry

    return m    

def circle(cx, cy, r, x, y):
    return math.sqrt((cx-x)**2 + (cy-y)**2) <= r

def build_priority_matrix_test(clients, salesman, sales_territories, perc_inside = 0.1):
    # Matrix
    m = np.zeros((len(salesman), len(clients)))

    # Rep
    for s in range(len(salesman)):
        # Cli
        for t in range(len(clients)):
            inside = circle(0.5, 0.5, 0.3, clients[t].lat, clients[t].lon)
                
            if not inside:
                if sales_territories[t] == s:
                    m[s, t] = 1
                else:
                    m[s, t] = perc_inside
            else:
                if sales_territories[t] == s:
                    m[s, t] = perc_inside
                else:
                    m[s, t] = 1
    return m    

# Save the original salesterritory and optimization salesterritory
#
#
def save_sales_territory(path, clients_index, salesman_index,  
                            initial_territory, best_territory):
  log('save result in /'+str(path)+'..')
  # Create path
  try:
      os.makedirs(path)
  except:
      pass


  ori_sales_territory = []
  opt_sales_territory = []

  for i in range(len(initial_territory)):

    ori_salesman = salesman_index[initial_territory[i]]
    opt_salesman = salesman_index[best_territory[i]]

    ori_sales_territory.append([clients_index[i], ori_salesman])
    opt_sales_territory.append([clients_index[i], opt_salesman])


  df_ori = pd.DataFrame(ori_sales_territory, columns=['client_id', 'salesman_id'])
  df_opt = pd.DataFrame(opt_sales_territory, columns=['client_id', 'salesman_id'])

  df_ori.to_csv(str(path)+'/original_salesterritory.csv')
  df_opt.to_csv(str(path)+'/optimized_salesterritory.csv')


def create_salesterritory_df(salesman_index, values_after):
  
  data = []
  for k in list(values_after.keys()):
    salesman = salesman_index[k]
    value    = values_after[k]

    data.append([salesman, value])

  return pd.DataFrame(data, columns = ['salesman_id', 'value'])

def create_history_df(history):
  return pd.DataFrame(history, columns =['avg_fitness'])

def log(txt):
  print(txt)

def plot_scatter(territory, salesman, sales_territories):
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(1, 1, 1)

    x     = []
    y     = []
    size  = []
    colors = []
    
    for client in range(len(sales_territories)):
        s      = sales_territories[client]
        x.extend([territory[client].lat])
        y.extend([territory[client].lon])
        size.extend([territory[client].benefit])
        colors.append(Category10[5][s])
    #plt.subplot(211)             # the first subplot in the first figure
    plt.scatter(x, y, s=size, c=colors, alpha=0.8)
    
    #plt.subplot(212)             # the second subplot in the first figure
    sx = []
    sy = []
    for sale in salesman:
        sx.append(sale.lat)
        sy.append(sale.lon)
        
    plt.scatter(sx, sy, s=500, marker='^', c='red')
    
    circ = plt.Circle((0.5,0.5),radius=0.3, color='g', fill=False)
    ax.add_patch(circ)
    
    plt.show()