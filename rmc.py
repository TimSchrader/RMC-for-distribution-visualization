from random import uniform
from random import randrange
from random import gauss

def rmc(nSize,nOfSteps,nOfConstr,starts,ends,fracts,weights) -> list:
    '''runs Reverse Monte Carlo'''
    
    # initialize distribution
    distr=[]
    indexOfBiggestRange=0
    biggestRange=0
    for i in range(nOfConstr):
        if ends[i]-starts[i] > biggestRange:
            indexOfBiggestRange=i
            biggestRange=ends[i]-starts[i]
    minimum = starts[indexOfBiggestRange]
    maximum = ends[indexOfBiggestRange]
    for j in range(nSize):
        distr.append(uniform(minimum,maximum))
    
    # estimate step size
    stepSizeFactor = biggestRange*0.09

    # assume initial guess to be worst possible
    previousBadness = sum(weights)

    # division outside of main loop
    fracOfPointInDistr = 1.0/nSize

    # main loop
    for k in range(nOfSteps):
        # move one data point at random
        iOfRandDistr = randrange(0,nSize)
        randStep = gauss(0,stepSizeFactor)
        distr[iOfRandDistr] += randStep

        # discard if out of bounds
        if distr[iOfRandDistr] < minimum or distr[iOfRandDistr] > maximum:
            distr[iOfRandDistr] -= randStep
            continue

        # evaluate new distr
        newBadness = 0
        for m in range(nOfConstr):
            fracInRange=0
            for n in range(nSize):
                if starts[m] < distr[n] and distr[n] < ends[m]:
                    fracInRange += fracOfPointInDistr
            newBadness += weights[m] * abs(fracts[m]-fracInRange)
        
        # reverse the move if it made the distribution worse
        if newBadness > previousBadness :
            distr[iOfRandDistr] -= randStep
        else:
            previousBadness = newBadness
    
    return distr
