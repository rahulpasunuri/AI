'''
This file contains support code for B551 Hw6                                 # File version:  November 19, 2015                                            #

For questions related to genetic algorithms or the knapsack problem, any AI can be of help. For questions related to the support code itself, contact Alex at aseewald@indiana.edu.
'''
import math
import random
import pickle
import numpy as np
import pandas as pd
from scipy.stats import norm

bits = [False, True]
elitismPercentage = 15


def performMutation(chromosomes, mutation_prob):
    ret = []
    for chrom in chromosomes:
        for bit in chrom:
            if random.random() < mutation_prob:
                #perform mutation..
                if chrom[bit] == False:
                    chrom[bit] = True
                else:
                    chrom[bit] = False
        ret.append(chrom)

    return ret

def getElites(chromosomes, fitnesses):
    maxEliteCount = int(elitismPercentage/100.0 * len(fitnesses)) + 1
    top_fitnesses = sorted(fitnesses)[-maxEliteCount:]
    elites = []
    currEliteCount = 0
    for i in range(len(fitnesses)):
        if fitnesses[i] in top_fitnesses and currEliteCount < maxEliteCount:
            elites.append(chromosomes[i])
            currEliteCount += 1
    return elites

def fitness(max_volume,volumes,prices):
    '''
    This should return a scalar which is to be maximized.
    max_volume is the maximum volume that the knapsack can contain.
    volumes is a list containing the volume of each item in the knapsack.
    prices is a list containing the price of each item in the knapsack, which is aligned with 'volumes'.
    '''
    totalVolume = sum(volumes)
    if totalVolume > max_volume:
        return 0 #fitness 0 will make sure that this chromosome will not be picked for elitism or crossover..

    return sum(prices)


def randomSelection(population,fitnesses):
    '''
    This should return a single chromosome from the population. The selection process should be random, but with weighted probabilities proportional
    to the corresponding 'fitnesses' values.
    '''
    #implementing the roulette wheel selection mechanism here..
    sum_fitnesses = int(sum(fitnesses)) #convert the sum to integer for simplicity
    #pick a number in the range o - fitnesses.
    pick = random.randint(0, sum_fitnesses)
    
    currSum = 0
    for i in range(len(population)):
        currSum += fitnesses[i]
        if pick < currSum:
            return population[i]
    
    #this happens when all the chromosomes have zero fitness!!        
    return random.choice(population)
    
def reproduce(mom,dad):
    #"This does genetic algorithm crossover. This takes two chromosomes, mom and dad, and returns two chromosomes."
    crossOverPos = random.randint(1, len(mom) - 1)
    rest = len(mom) - crossOverPos

    return (mom[:crossOverPos:] + dad[-rest:]), dad[:crossOverPos] + mom[-rest:]

def mutate(child):
    #"Takes a child, produces a mutated child." Just a single bit of the child..
    size = len(child)
    pos = randint(0, size)
    if child[pos] == True:
        child[pos] = False
    else:
        child[pos] = True
    return child

def compute_fitnesses(world,chromosomes):
    '''
    Takes an instance of the knapsack problem and a list of chromosomes and returns the fitness of these chromosomes, according to your 'fitness' function.
    Using this is by no means required, if you want to calculate the fitnesses in your own way, but having a single definition for this is convenient because
    (at least in my solution) it is necessary to calculate fitnesses at two distinct points in the loop (making a function abstraction desirable).

    Note, 'chromosomes' is required to be a 2D numpy array of boolean values (a fixed-size boolean array is the recommended encoding of a chromosome, and there should be multiple of these arrays, hence the matrix).
    '''

    for chromosome in chromosomes:
        fitness(world[0], np.array(world[1]) * np.array(chromosome), np.array(world[2]) * np.array(chromosome)) 
    
    return [fitness(world[0], np.array(world[1]) * np.array(chromosome), np.array(world[2]) * np.array(chromosome)) for chromosome in chromosomes]


def getInitPopulation(popsize, sizeOfChromosome, world):
    initPop = []
    for i in range(popsize):
        currChrom = []
        for pos in range(sizeOfChromosome):
            random.shuffle(bits)
            currChrom.append(bits[0])
        initPop.append(currChrom)            
        currFitness = compute_fitnesses(world, initPop)
        
        if sum(currFitness) == 0:
            #do the calculation again!!
            #this ensures that the initial population has some fit individuals!!
            return getInitPopulation(popsize, sizeOfChromosome, world)

    return initPop
    
def genetic_algorithm(world,popsize,max_years,mutation_probability):
    '''
    world is a data structure describing the problem to be solved, which has a form like 'easy' or 'medium' as defined in the 'run' function.
    The other arguments to this function are what they sound like.
    genetic_algorithm *must* return a list of (chromosomes,fitnesses) tuples, where chromosomes is the current population of chromosomes, and fitnesses is
    the list of fitnesses of these chromosomes. 
    '''
    random.seed()
    chromosomes = []
    fitnesses = []
    sizeOfChromosome = len(world[1])

    retVal = []
        
    initPop = getInitPopulation(popsize, sizeOfChromosome, world)
        
    stopGA = False
    currPopulation = initPop
    currFitness = None

    while len(retVal) < max_years:
        #TODO: do mutation on the current generation here..
        currPopulation = performMutation(currPopulation, mutation_probability)
        
        #compute fitnesses for the current generation..
        currFitness = compute_fitnesses(world, currPopulation)
        retVal.append((np.array(currPopulation), currFitness))
        
        #add elites
        children = getElites(currPopulation, currFitness)
        
        while len(children) < popsize:
            mom = randomSelection(currPopulation,currFitness)
            dad = randomSelection(currPopulation,currFitness)
            c1, c2 =  reproduce(mom,dad)
            children.append(c1)
            if len(children) == popsize:
                break
            children.append(c2)
        
        #update the variable being used..
        currPopulation = children
    
    #add the last generation to the list..
    currFitness = compute_fitnesses(world, currPopulation)
    retVal.append((np.array(currPopulation), currFitness))
    
    return retVal

def run(popsize,max_years,mutation_probability):
    '''
    The arguments to this function are what they sound like.
    Runs genetic_algorithm on various knapsack problem instances and keeps track of tabular information with this schema:
    DIFFICULTY YEAR HIGH_SCORE AVERAGE_SCORE BEST_PLAN
    '''
    table = pd.DataFrame(columns=["DIFFICULTY", "YEAR", "HIGH_SCORE", "AVERAGE_SCORE", "BEST_PLAN"])
    
    sanity_check = (10, [10, 5, 8], [100,50,80])
    chromosomes = genetic_algorithm(sanity_check,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'sanity_check', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)
            
    easy = (20, [20, 5, 15, 8, 13], [10, 4, 11, 2, 9] )
    chromosomes = genetic_algorithm(easy,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'easy', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)

    medium = (100, [13, 19, 34, 1, 20, 4, 8, 24, 7, 18, 1, 31, 10, 23, 9, 27, 50, 6, 36, 9, 15],
                   [26, 7, 34, 8, 29, 3, 11, 33, 7, 23, 8, 25, 13, 5, 16, 35, 50, 9, 30, 13, 14])
    chromosomes = genetic_algorithm(medium,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'medium', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)

    hard = (5000, norm.rvs(50,15,size=100), norm.rvs(200,60,size=100))
    chromosomes = genetic_algorithm(hard,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'hard', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)
    result = {}
    for difficulty_group in ['sanity_check','easy','medium','hard']:
        group = table[table['DIFFICULTY'] == difficulty_group]
        bestrow = group.ix[group['HIGH_SCORE'].argmax()]
        result[difficulty_group] = (int(bestrow['YEAR']), bestrow['HIGH_SCORE'], bestrow['BEST_PLAN'])
        print("Best year for difficulty {} is {} with high score {} and chromosome {}".format(difficulty_group,int(bestrow['YEAR']), bestrow['HIGH_SCORE'], bestrow['BEST_PLAN']))
    #table.to_pickle("results.pkl") #saves the performance data, in case you want to refer to it later. pickled python objects can be loaded back at any later point.
    return result

diffGroups = ['sanity_check','easy','medium','hard']
    
def main():
    #experiments with different popsize:
    final_results = {}
    final_results_reverse = {}
    best_results = {}
    
    for diff in diffGroups:
        #tuple is (generation, max_value, initpop, mutation)
        best_results[diff] = (1000, 0, 0, 0)
    
    
    for c in range(1, 10):
        initPop = c*5 # this is the initial population..
        final_results[initPop] = {}
        for prob in range(0, 10):
            # this is the mutation probability..
            mutation_prob = prob/10.0;
            
            if mutation_prob not in final_results_reverse:
                final_results_reverse[mutation_prob] = {}
            
            final_results[initPop][mutation_prob] = run(initPop, 100, mutation_prob)
            final_results_reverse[mutation_prob][initPop] = run(initPop, 100, mutation_prob)
            for diff in diffGroups:
                currResult = final_results[initPop][mutation_prob][diff]
                if  best_results[diff][1] < currResult[1]:
                    #update the best value for this difficulty level!!
                    best_results[diff] = (currResult[0], currResult[1], initPop, mutation_prob)
            #break
        #break

    #printing the best results..
    print "="*100
    print "Best Results overall are:"
    print "="*100
    
    for diff in diffGroups:
        print "-"*40
        print "For Difficulty:  ", diff
        print "\tMax value was:   ", best_results[diff][1]
        print "\tGeneration:      ", best_results[diff][0]
        print "\tInit Population: ", best_results[diff][2]
        print "\tMutation Prob    :", best_results[diff][3]
        print "-"*40
        print

    print 
    print
    print "="*100
    print "Results with varying initial Population are: (averaged across multiple mutation probabilities)"
    print "="*100

    #compute averages for the init pop..
    for diff in diffGroups:
        print "-"*40
        print "For Difficulty:  ", diff
        print

        popList = []        
        for initPop in final_results:
            popList.append(initPop)

        #sort the population list..
        popList = sorted(popList)
        for initPop in popList:
            print "-"*40
            print "For Init Population: ", initPop
            t = final_results[initPop]
            avg_Value = 0
            avg_year = 0
            for el in final_results[initPop]:
                avg_year += final_results[initPop][el][diff][0]
                avg_Value += final_results[initPop][el][diff][1]
             
            avg_Value = (avg_Value*1.0)/len(final_results[initPop])
            avg_year = (avg_year*1.0)/len(final_results[initPop])
            print "\tAvg. Value is: ",avg_Value
            print "\tAvg. Year is: ",avg_year
            print "-"*40
            print 
    
    print 
    print
    print "="*100
    print "Results with varying mutation probabilities are: (averaged across multiple initial populations..)"
    print "="*100

    #compute averages for the init pop..
    for diff in diffGroups:

        print "For Difficulty:  ", diff
        print        
        mutList = sorted([mutProb for mutProb in final_results_reverse])
        
        for mutProb in mutList:
            print "-"*40
            print "For Mutation: ", mutProb
            t = final_results_reverse[mutProb]
            avg_Value = 0
            avg_year = 0
            for el in final_results_reverse[mutProb]:
                avg_year += final_results_reverse[mutProb][el][diff][0]
                avg_Value += final_results_reverse[mutProb][el][diff][1]
            
            avg_Value = (avg_Value*1.0)/len(final_results_reverse[mutProb])
            avg_year = (avg_year*1.0)/len(final_results_reverse[mutProb])
            print "\tAvg. Value is: ",avg_Value
            print "\tAvg. Year is: ",avg_year
            print "-"*40
            print 
    

if __name__ == "__main__" : main()
