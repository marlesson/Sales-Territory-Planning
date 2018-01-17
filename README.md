# Otimização na Reconfiguração de Território de Vendas utilizando Algoritmos Genéticos

O planejamento de território para vendas pode ser formulado como um problema de otimização, em que cada território (cidade, bairro, rua, cliente.. etc) deve ser alocado para um **melhor representante** de acordo com alguns critérios e restrições.

Usualmente o planejamento é realizado a cada período de tempo (um ano, uma semana... ), levando em consideração o tempo necessário para o representante visitar todos os territórios de vendas.

O objetivo da otimização depende do problema, mas de forma geral são otimizadas características como:

* Minimização da distância percorrida, ou seja, manter territórios compáctos
* Balanceamento de tempo de trabalho/atendimento
* Balanceamento dos ganhos em cada território

## Modelo Matemático
...
#### Balenceamento de Benefício
...
#### Minimização da Distância
...
#### Maximização da Prioridade
...
#### Balanceamento de Tempo de Atendimento
...
## Como Usar

A utilização é realizada por meio de script, com arquivos de entrada (configuração atual e prioridades) e arquivos de saída com diversos resultados, como principais o `'optimized_salesterritory.csv'` que contem a nova configuração do território de vendas e o `'avg_fitness.csv'` que exibe a evolução da otimização ao longo das gerações.

### Parâmetrização

* Parametrização de execução da biblioteca, com definição de parametrização do Algoritmo Genético e do problema de
territorio de vendas com o balanceamento entre as prioridades.

```/conf.yml```

```yarn
# Genetic Algorithm Params
#
#
genetic_algorithm:
  init_population: 500
  generations: 300
  prob_crossover: 0.9
  prob_mutation: 0.2
  in_vitro: False  


# Problem Sales Territory Params
#
#
problem:
  cost_per_km: 1.78
  max_clients: 120
  min_clients: 50
  min_faturamento: 1000
  fitness_weights:
    balance_total_client: 0.01
    balance_benefit:   0.01
    balance_workload:  0.02
    minimize_distance: 0.25
    maximize_priority: 0.7
```

### Input

A entrada para a a otimização é um dataset com os dados atuais do territorio de vendas, e um dataset de prioridade quando utilizado.

#### Dataset

Lista de territórios que devem ser reconfigurados

```
client_id             3922 non-null int64
client_lat            3922 non-null float64
client_lon            3922 non-null float64
client_revenue_avg    3922 non-null float64
salesman_id           3922 non-null int64
salesman_lon          3922 non-null float64
salesman_lat          3922 non-null float64
salesman_cost         3922 non-null float64
visit_in_month        3922 non-null int64
time_to_attend        3922 non-null int64
```

#### Matrix de Prioridade

A matriz de prioridade não é obrigatória para ã execução da otimização, sendo apenas uma forma de priorizar algumas modificações entre territórios e representantes.
Lista de prioridades para a reconfiguração

```
client_id      258852 non-null int64
salesman_id    258852 non-null int64
priority       258852 non-null float64
```

### Run

```sh
$ python run.py -h
```

```
usage: run.py [-h] [--input INPUT] [--priority PRIORITY] [--output OUTPUT]
              [--params PARAMS]

Process some integers.

optional arguments:
  -h, --help           show this help message and exit
  --input INPUT        File with data
  --priority PRIORITY  File with Priority matrix
  --output OUTPUT      Output Path
  --params PARAMS      Configuration
```

* Execução 

```$ python run.py --input input/input_dataset.csv --priority input/priority_abc.csv --output output/test```

### Output


* avg_fitness.csv
* f1_fitness.csv
* f2_fitness.csv
* f3_fitness.csv
* f4_fitness.csv
* f5_fitness.csv
* optimized_benefit_per_salesman.csv
* optimized_dist_per_salesman.csv
* optimized_salesterritory.csv
* optimized_sustainability_per_salesman.csv
* optimized_total_clients_per_salesman.csv
* optimized_workload_per_salesman.csv
* original_benefit_per_salesman.csv
* original_dist_per_salesman.csv
* original_salesterritory.csv
* original_sustainability_per_salesman.csv
* original_total_clients_per_salesman.csv
* original_workload_per_salesman.csv

...
#### optimized_salesterritory.csv

Arquivo contendo a reconfiguração do território de vendas após a otimização.

```
client_id      258852 non-null int64
salesman_id    258852 non-null int64
```

## Referências

