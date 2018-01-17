# bin/bash
# floyd run "bash run_all.sh" --data marlesson/datasets/ga-sales-territory/5:input

# parser.add_argument('--prob_mutation', type=float, default=0.2)
# parser.add_argument('--prob_crossover', type=float, default=0.9)
# parser.add_argument('--generations', type=int, default=100)
# parser.add_argument('--init_population', type=int, default=800)
# parser.add_argument('--elitism', type=int, default=1)
# parser.add_argument('--local_search', type=bool, default=False)

prob_mutation='0.2'
prob_crossover='0.99'
init_population='1500'
generations='500'
inputs='input_dataset_go_shuffle'
local_search=true

for m in $prob_mutation; do
  for c in $prob_crossover; do
    for p in $init_population; do
      for g in $generations; do
        for f in $inputs; do
          python run_ga.py --input '/input/'$f'.csv' --prob_mutation $m --output '/output/'$f'_'$m'_'$c'_'$p'_'$g'_norm'  \
            --prob_crossover $c --init_population $p --generations $g > '/output/'$f'_'$m'_'$c'_'$p'_'$g'_norm.log'

          # python run_ga.py --input '/input/'$f'.csv'  --prob_mutation $m --output '/output/'$f'_'$m'_'$c'_'$p'_'$g'_pry'  \
          #   --prob_crossover $c --init_population $p --local_search true --generations $g --priority /input/priority_abc.csv  > '/output/'$f'_'$m'_'$c'_'$p'_'$g'_pry.log'
        done
      done
    done
  done
done

