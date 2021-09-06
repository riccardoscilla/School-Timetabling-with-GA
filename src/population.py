import multiprocessing
from functools import partial
import random
import copy
from itertools import combinations
from individual import individual

from operator import itemgetter # to get key with min value in dict

class population:
    def __init__(self, args):        
        self.pop_size = args["pop_size"]
        self.cpu = args["cpu"]
        self.t_size = args["t_size"]
        self.hill_climb = args["hill_climb"]
        self.swaps = args["swaps"]

        self.pop = None

        self.best_ind = None
        self.best_fitness = None
        self.best_tot_fitness = None

        self.diversity = None
        self.equal_ind = None

        self.parents = None

        self.init_population_mp(args)
        self.find_best_individual()

    def init_population_mp(self,args):
        pool = multiprocessing.Pool(processes=self.cpu)
        func = partial(individual, args)
        self.pop = pool.map(func,range(self.pop_size))
        pool.close()
        pool.join()

    def find_best_individual(self):
        fit_map = {}
        for ind in self.pop:
            fit_map[ind] = ind.tot_fitness
        self.best_ind = min(fit_map.items(), key=itemgetter(1))[0]
        self.best_fitness = self.best_ind.fitness
        self.best_tot_fitness = self.best_ind.tot_fitness

    def find_pop_diversity(self):

        self.equal_ind = 0
        unique_pop = []

        for pair in combinations(self.pop, r=2):
            ind1 = pair[0].flat_TT
            ind2 = pair[1].flat_TT

            if ind1.equals(ind2):
                if pair[0] not in unique_pop:
                    self.equal_ind += 1
                    unique_pop.append(pair[0])
                if pair[1] not in unique_pop:
                    self.equal_ind += 1
                    unique_pop.append(pair[1])

        print("# ind", len(self.pop), "Equal",self.equal_ind)        

    def tournament_selection(self):
        self.parents = []
        for _ in range(self.pop_size):
            fit_tournament = {}
            for ind in random.sample(self.pop, self.t_size):
                fit_tournament[ind] = ind.tot_fitness
            champion = min(fit_tournament.items(), key=itemgetter(1))[0]

            self.parents.append(champion)

    def variation_tournament_selection(self):
        self.parents = []
        for _ in range(self.pop_size):
            champion = random.choice(self.pop)
            for _ in range(self.t_size-1):
                contender = random.choice(self.pop)
                choice = random.choice([1,2,3])
                if   choice == 1: continue
                elif choice == 2: champion = contender
                elif choice == 3 and contender.tot_fitness < champion.tot_fitness: champion = contender
            self.parents.append(champion)         

    def HillClimb(self,parent):
        HCSteps = 0
        offspring = copy.deepcopy(parent)

        while parent.tot_fitness <= offspring.tot_fitness and HCSteps < 10:
            offspring = copy.deepcopy(parent) # restart from parent
            
            for _ in range(self.swaps):
                prev_offspring = copy.deepcopy(offspring)

                # mutate offspring
                if offspring.tot_fitness > 100:
                    offspring.offspring_worst_rand_swap() 
                else:
                    offspring.offspring_rand_swap()

                if prev_offspring.tot_fitness < offspring.tot_fitness: # if ind before mutation was better, reject swap
                    offspring = copy.deepcopy(prev_offspring)

            HCSteps += 1
            
        return offspring

    def notHillClimb(self,parent):
        offspring = copy.deepcopy(parent)

        for _ in range(self.swaps):
            prev_offspring = copy.deepcopy(offspring)

            # mutate offspring
            if offspring.tot_fitness > 100:
                offspring.offspring_worst_rand_swap() 
            else:
                offspring.offspring_rand_swap()

            if prev_offspring.tot_fitness < offspring.tot_fitness: # if ind before mutation was better, reject swap
                offspring = copy.deepcopy(prev_offspring)
        
        return offspring
        
    def mutate_mp(self):
        if self.hill_climb:
            pool = multiprocessing.Pool(processes=self.cpu)
            self.pop = pool.map(self.HillClimb,self.parents)
            pool.close()
            pool.join()
        else:
            pool = multiprocessing.Pool(processes=self.cpu)
            self.pop = pool.map(self.notHillClimb,self.parents)
            pool.close()

    def elitism(self):
        self.pop.append(self.best_ind)