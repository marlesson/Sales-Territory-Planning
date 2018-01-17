m='0.2'
c='1'
p='5000'
g='2000'
f='input_dataset_go'

python run.py --input '/input/'$f'.csv' --local_search true --prob_mutation $m --output '/output/'$f'_'$m'_'$c'_'$p'_'$g'_norm'  \
  --prob_crossover $c --init_population $p --generations $g > '/output/'$f'_'$m'_'$c'_'$p'_'$g'_norm.log'

python run.py --input '/input/'$f'.csv' --local_search true --prob_mutation $m --output '/output/'$f'_'$m'_'$c'_'$p'_'$g'_pry'  \
  --prob_crossover $c --init_population $p --generations $g --priority /input/priority_abc.csv  > '/output/'$f'_'$m'_'$c'_'$p'_'$g'_pry.log'
