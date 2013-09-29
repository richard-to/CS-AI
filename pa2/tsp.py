from math import exp, expm1
from random import randint, random, sample, seed, shuffle


def generateCostGrid(n=10, min=100, max=2500):
    return [[randint(min, max) for g in xrange(n)] for i in xrange(n)]


def generateTour(n=10):
    tour = range(n)
    shuffle(tour)
    return tour


def calcCost(tour, grid):
    start = tour[0]
    cost = 0
    for dest in tour[1:]:
        cost += grid[start][dest]
        start = dest
    return cost


def printCostGrid(grid):
    for row in grid:
        print row


def getTourPermutations(tour, grid):
    currentTour = []
    currentCost = 0
    tourPermutations = []
    n = len(tour)
    for i in xrange(n):
        for g in xrange(i + 1, n):
            currentTour = swap(tour, i, g)
            currentCost = calcCost(currentTour, grid)
            tourPermutations.append([currentCost, currentTour])
    return tourPermutations


def pickNextStep(cost, tour, grid):
    bestTour = tour
    bestCost = cost
    tourPermutations = getTourPermutations(tour, grid)
    for currentTour in tourPermutations:
        if currentTour[0] < bestCost:
            bestCost = currentTour[0]
            bestTour = currentTour[1]
    return [bestCost, bestTour]


def swap(tour, i, g):
    currentTour = list(tour)
    tempCity = currentTour[i]
    currentTour[i] = currentTour[g]
    currentTour[g] = tempCity
    return currentTour


def runHillClimbing(grid):
    tour = generateTour(len(grid))
    cost = calcCost(tour, grid)
    bestTour = [cost, tour]

    while True:
        nextStep = pickNextStep(bestTour[0], bestTour[1], grid)
        if nextStep[0] < bestTour[0]:
            bestTour = nextStep
        else:
            break
    return bestTour


def runRandomRestartHillClimbing(grid, runs=50):
    bestTour = runHillClimbing(grid)
    for i in xrange(runs - 1):
        nextTour = runHillClimbing(grid)
        if nextTour[0] < bestTour[0]:
            bestTour = nextTour
    return bestTour


def costFunction3(time):
    return 2500 * exp(-0.0000002 * time**2 - 0.000001*time)


def costFunction2(time):
    return 2500 - 0.0002 * time**2


def costFunction(time):
    return 2500 - time


def runSimulatedAnnealing(grid, costFunction=costFunction3):
    k = 2
    tour = generateTour(len(grid))
    bestTour = [calcCost(tour, grid), tour]
    nextTour = bestTour
    t = 0
    while True:
        T = costFunction(t)
        if T <= 0:
            return bestTour

        tourPermutations = getTourPermutations(nextTour[1], grid)
        shuffle(tourPermutations)
        for currentTour in tourPermutations:
            if currentTour[0] <= nextTour[0]:
                nextTour = currentTour
                if nextTour[0] < bestTour[0]:
                    bestTour = nextTour
                break
            else:
                result = abs(currentTour[0] - nextTour[0])/T
                if result < 13 and 1/exp(result) >= random():
                    nextTour = currentTour
                    if nextTour[0] < bestTour[0]:
                        bestTour = nextTour
                    break
        t += 1
    return bestTour


def main():
    seed(10)
    n = 10
    costGrid = generateCostGrid(n)
    printCostGrid(costGrid)
    print runRandomRestartHillClimbing(costGrid)
    print runSimulatedAnnealing(costGrid)


if __name__ == '__main__':
    main()