#!/usr/bin/python

""" Genetic Algorithm """

import data
import fitness
import population
import copy
import sys

### Functions ###

# 
def f(x):
    """
    Utility mapping to convert model complexity
    to number of genes required per chromosome
    """
    key = str(x)
    return {
      1:7,
      2:14,
      3:21,
      4:8,
      5:15,
      6:22,
    }[x]

def printFVals(fVals):
    """
    Utility function to clean up printing of different
    F vals for each model's output
    """
    results = ''
    info = sorted(fVals.items())
    for pair in info:
        results += (str(pair[0]) + ": F1= " + str(pair[1][0]) + " F2= " + str(pair[1][1]) + '\n')
    return results


def runGA():
    """ 
    Genetic Algorithm Engine

    This script will run GA on each of our models, writing out the result
    """
    pass


### Start of Engine Script ###

if len(sys.argv) != 4:
    print "Usage: ./ga.py modelComplexity path/to/out/ generations"
    print "Model Complexities"
    print "1-3: No Y intercept 4-6: Y intercept"
    print "1,4- Linear 2,5- Quadratic 3,6- Cubic"
    sys.exit(1)

model = int(sys.argv[1])

outFilePath = sys.argv[2]
generations = int(sys.argv[3])

c8 = data.DataSet('C8')
R = data.DataSet('R')
M = data.DataSet('M')
T = data.DataSet('T')

dataSetList = [c8, R, M, T]
for elem in dataSetList:
    elem.setModel(model)


FIT = fitness.Fitness(True)
pop1 = population.Population(12,4.0,200,numGenes=f(model),initialize=True)
pop2 = population.Population(12,4.0,200,numGenes=f(model),initialize=False)
outFH = open(outFilePath,'w')
for elem in pop1:
    elem.fitness = FIT.calculateTotalFitness(elem,dataSetList)
pop1.sortPopulation()
outFH.write('Starting Population \n')
outFH.write(pop1.topBetas())
outFH.write(printFVals(pop1.pop[0].fVals))

count = 0
for i in xrange(generations):
    print "Generation: " + str(i)
    pop2.stepGeneration(pop1)
    for elem in pop2:
        elem.fitness = FIT.calculateTotalFitness(elem,dataSetList)
    pop2.sortPopulation()
    outFH.write(pop2.topBetas())
    outFH.write(printFVals(pop1.pop[0].fVals))
    if pop1.pop[0].genes != pop2.pop[0].genes:
        print "Updated Top Beta
    pop1 = copy.deepcopy(pop2)

pop1.sortPopulation()
outFH.write('\n\nFinal\n')
topPop=pop1.pop[0]
outFH.write(str(topPop.betas()) + '\n')
outFH.write(printFVals(pop1.pop[0].fVals))

# Calculate C9 info
c9 = data.DataSet('C9')
c9.setModel(model)
topFitC9 = FIT.calculateFitness(topPop,c9)
outFH.write('F1 = ' + str(-topFitC9[0]) + ' F2 = ' + str(topFitC9[1]) + '\n')
ZFinal = FIT.calculateZScore(topPop,dataSetList,model)
outFH.write('Per File:' + str(ZFinal[0]) + '\n')
outFH.write('Zavg: ' + str(ZFinal[1]))
outFH.close()


