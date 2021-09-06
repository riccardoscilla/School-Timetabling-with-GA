from import_list import *
from population import population
from datetime import datetime, timedelta
import multiprocessing
import sys
import random

import matplotlib.pyplot as plt
import numpy as np

def stop_condition(pop):
    if  pop.best_fitness["HC1"]==0 and \
        pop.best_fitness["HC2"]==0 and \
        pop.best_fitness["HC3"]==0 and \
        pop.best_fitness["SC1_max"]<=5:
        return True 
    return False

def run(args):
    print("Main seed:",args["seed"])

    time_pop = datetime.now()
    pop = population(args)
    print(datetime.now()-time_pop)

    # print(pop.best_fitness, pop.best_tot_fitness)

    i = 0
    while not stop_condition(pop):
    # while datetime.now() - time_pop < timedelta(minutes=20):
    # while i < args["n_gen"]:
        # if stop_condition(pop):
        #     break
        i+=1

        print("\nGeneration",i)
        time_gen = datetime.now()

        pop.find_pop_diversity()

        # pop.tournament_selection()
        pop.variation_tournament_selection()
        
        pop.mutate_mp()

        pop.elitism()

        pop.find_best_individual()

        print(pop.best_fitness)
        print("tot fitness",pop.best_tot_fitness)
        print(datetime.now()-time_gen)

    # show best
    print("-----------------------------------------------")
    print("Best individual")
    print(pop.best_fitness, pop.best_tot_fitness)
    print(datetime.now()-time_pop)


if __name__ == '__main__':

    args = {}
    args["fname"] = "./data.csv"
    args["fixed_fname"] = "./fixed_data.csv"

    args["pop_size"] = 20
    args["n_gen"] = 50

    args["cpu"] = 5

    args["seed"] = random.randint(0,sys.maxsize) // args["pop_size"]

    args["t_size"] = int(0.2*args["pop_size"]) if args["pop_size"]>=10 else 1
    args["hill_climb"] = True
    args["swaps"] = 10

    run(args)

    