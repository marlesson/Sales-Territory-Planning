# bin/bash

# floyd run "bash run_all_tabu.sh" --data marlesson/datasets/ga-sales-territory/2:input
# parser.add_argument('--tabu_size', type=int, default=50)
# parser.add_argument('--interactions', type=int, default=1000)

# tabu_size='10 100 500'
# interactions='1000 2000 4000'
# inputs='input_dataset_5 input_dataset_10'

tabu_size='100'
interactions='1500'
inputs='input_dataset_31'

for s in $tabu_size; do
  for i in $interactions; do
    for f in $inputs; do
      python run_tabu.py --input '/input/'$f'.csv' --tabu_size $s --output '/output/'$f'_'$s'_'$i'_norm'  \
        --interactions $i  > '/output/'$f'_'$s'_'$i'_norm.log'

      python run_tabu.py --input '/input/'$f'.csv' --tabu_size $s --output '/output/'$f'_'$s'_'$i'_pry'  \
       --interactions $i --priority /input/priority_abc.csv  > '/output/'$f'_'$s'_'$i'_pry.log'
    done
  done
done

