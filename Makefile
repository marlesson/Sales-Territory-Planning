
help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "build - package"

all: default

floyd-ga:
	#floyd run --cpu "python run.py --input /input/input_dataset_go.csv --priority /input/priority_abc.csv --prob_mutation 0.2 --output /output/ --prob_crossover 0.9 --init_population 1000 --generations 1500  > '/output/normal.log'" --data marlesson/datasets/ga-sales-territory/3:input
	floyd run --cpu "python run.py --input /input/input_dataset_go.csv --prob_mutation 0.3 --output /output/ --prob_crossover 0.9 --init_population 1000 --generations 1500  > '/output/normal.log'" --data marlesson/datasets/ga-sales-territory/6:input

floyd-tabu:
	#floyd run --cpu "python run_tabu_search.py --input --priority /input/priority_abc.csv /input/input_dataset_go.csv --tabu_size 100 --output /output/ --iterates 2000  > '/output/normal.log'" --data marlesson/datasets/ga-sales-territory/3:input
	floyd run --cpu "python run_tabu_search.py --input /input/input_dataset_go.csv --tabu_size 100 --output /output/ --iterates 1000  > '/output/normal.log'" --data marlesson/datasets/ga-sales-territory/6:input

floyd-ga-all:
	floyd run --cpu+ "bash run_all_ga.sh" --data marlesson/datasets/ga-sales-territory/6:input

floyd-tabu-all:
	floyd run --cpu+ "bash run_all_tabu.sh" --data marlesson/datasets/ga-sales-territory/6:input