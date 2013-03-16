import numpy as np
import scipy.stats as stats
""" implementation for a fitness calculator

We will take a given chromosome and a given dataSet and calculate it's total fitness

TFdataset = -F1 + F2
F2 is the average of all of the data set's lowest TMScore - index lowest
Ebetter and use it to average
F1 = PCC(ALL Ebetter, ALL TMscores)[0] (Maybe weight?)

"""
class Fitness(object):

    def __init__(self,logging):
        self.logging = logging
        if logging:
            self.output = open('Fscores.txt','w')

    def calculateTotalFitness(self,_betas,_dataSetList):
        #Calculates Total Fitness
        #    _betas is a numpy array
        #    _dataSetList is a list of DataSet objects

        totalNumProts = sum([x.numProts for x in _dataSetList])
        # Weighted average of dataSets
        totalFitness = 0.0
        tFact =0.0

        for elem in _dataSetList:
            # Weighting our code with a dataset size average + an ordering
            factor = self.weight(elem.name) + (elem.numProts / totalNumProts)
            elemFit = self.calculateFitness(_betas,elem)
            totalFitness += (factor * elemFit)

        #return totalFitness
        return totalFitness

    def calculateFitness(self,_betas,_dataSet):
        #Calculates the fitness for an individual dataSet
        #    _betas is a numpy array
        #    _dataSet is a single dataset object
        #
        #    fitness = -F1 + F2
        #    F2 = mean of TMscore indexed from lowest Ebetter 
        sumTMScores = 0.0
        eBetterList = []
        tmScoreList = []

        for protein in _dataSet:
            eBetter = np.dot(protein.eData,_betas)
            indexTM = np.argmin(eBetter)
            sumTMScores += protein.TMScore[indexTM]
            eBetterList.append(eBetter)
            tmScoreList.append(protein.TMScore)

        f1 = stats.pearsonr(np.concatenate(eBetterList),
                               np.concatenate(tmScoreList))[0]

        f2 = sumTMScores / _dataSet.numProts
        fitness = -f1 + f2

        if self.logging:
            self.output.write('\n' + _dataSet.name +'\n')
            self.output.write('F1 = ' + str(f1) + '\n')
            self.output.write('F2 = ' + str(f2) + '\n')

        return fitness

    def updateFitness(self,_pop,_dataSetList):
        for chromosome in _pop:
            chromosome.fitness = self.calcuateTotalFitness(chromosome.betas(),_dataSetList)
        _pop.sortPopulation()

    def weight(self,x):
        # Utility switch function 
        return {
            'M': 1.,
            'C8': 2.,
            'T': 3.,
            'R': 4.,
        }[x]
