import sys
from math import exp, expm1
from random import randint, random, sample, seed, shuffle


def getCityNames():
    """
    Gets a list of city names to use in place of array indexes.

    Index 0 of the array would equal "Anchorage". Index 1 would equal "New York".

    Can only be used if the matrix size is less than equal to 50

    Return:
        List of city names
    """
    return [
        "Anchorage",
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Philadelphia",
        "Phoenix",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
        "Jacksonville",
        "Indianapolis",
        "San Francisco",
        "Austin",
        "Columbus",
        "Fort Worth",
        "Charlotte",
        "Detroit",
        "El Paso",
        "Memphis",
        "Baltimore",
        "Boston",
        "Seattle",
        "Washington",
        "Nashville-Davidson",
        "Denver",
        "Louisville-Jefferson County",
        "Milwaukee",
        "Portland",
        "Las Vegas",
        "Oklahoma City",
        "Albuquerque",
        "Tucson",
        "Fresno",
        "Sacramento",
        "Long Beach",
        "Kansas City",
        "Mesa",
        "Virginia Beach",
        "Atlanta",
        "Colorado Springs",
        "Omaha",
        "Raleigh",
        "Miami",
        "Cleveland",
        "Tulsa",
        "Oakland",
        "Minneapolis",
        "Wichita",
        "Arlington"
    ]


def generateCostGrid(n=10, min=100, max=2500):
    """
    Generates a 2-d array to use as the cost grid.

    Args:
        n: The size of the cost grid. Creates an n x n matrix
        min: Minimum cost. Inclusive. Should be less than max cost
        max: Maximum cost. Inclusive.
    """
    return [[randint(min, max) for g in xrange(n)] for i in xrange(n)]


def generateTour(n=10):
    """
    Generates a random tour for the initial cost

    Args:
        n: Column/Row size of matrix. Should be the same as used to generate grid

    Returns:
        An array of values from 0 to n-1. The values will be in random order.
    """
    tour = range(1, n)
    shuffle(tour)
    tour.insert(0, 0)
    return tour


def calcCost(tour, grid):
    """
    Calculates the cost a tour based on the cost grid.

    Basically add cost from index 0 to 1,  1 to 2, 2 to 3,..., and n-1to 0.

    Args:
        tour: An array of values from 0 to n-1 and size n
        grid: Cost matrix with size n x n

    Returns:
        Cost of tour
    """
    start = tour[0]
    cost = 0
    for dest in tour[1:]:
        cost += grid[start][dest]
        start = dest
    cost += grid[-1][0]
    return cost


def printCostGrid(grid):
    """
    Prints the costs of the cost matrix to the console.

    Args:
        grid: Cost matrix
    """
    for row in grid:
        print row


def getTourPermutations(tour, grid):
    """
    Generates all tour permutations possibly from swapping two indexes

    Args:
        tour: Current tour
        grid: Cost matrix

    Returns:
        An array of all permutations of a current tour
    """
    currentTour = []
    currentCost = 0
    tourPermutations = []
    n = len(tour)
    for i in xrange(1, n):
        for g in xrange(i + 1, n):
            currentTour = swap(tour, i, g)
            currentCost = calcCost(currentTour, grid)
            tourPermutations.append([currentCost, currentTour])
    return tourPermutations


def pickNextStep(cost, tour, grid):
    """
    Picks the next best tour based on lowest cost

    Args:
        cost: Current best cost
        tour: Current best tour
        grid: Cost grid

    Returns:
        An list with best cost and best tour
    """
    bestTour = tour
    bestCost = cost
    tourPermutations = getTourPermutations(tour, grid)
    for currentTour in tourPermutations:
        if currentTour[0] < bestCost:
            bestCost = currentTour[0]
            bestTour = currentTour[1]
    return [bestCost, bestTour]


def swap(tour, i, g):
    """
    Swaps values for two indexes

    Args:
        tour: Current tour
        i: Index to swap with index g
        g: Index to swap with index i

    Returns:
        New tour with swapped indexes
    """
    currentTour = list(tour)
    tempCity = currentTour[i]
    currentTour[i] = currentTour[g]
    currentTour[g] = tempCity
    return currentTour


def runHillClimbing(grid, tour=None):
    """
    Runs basic hill climbing algorithm.

    Keep searching until we reach a
    local minima.

    Args:
        grid: Cost grid
        tour: Initial tour. If None, then a random tour will be generated

    Returns:
        The best tour found
    """
    tour = tour if tour is not None else generateTour(len(grid))
    cost = calcCost(tour, grid)
    bestTour = [cost, tour]

    while True:
        nextStep = pickNextStep(bestTour[0], bestTour[1], grid)
        if nextStep[0] < bestTour[0]:
            bestTour = nextStep
        else:
            break
    return bestTour


def runRandomRestartHillClimbing(grid, tour=None, restarts=50):
    """
    Runs hill climbing with random restart.

    Basically the same as hill climbing, except we run
    hill climbing more than once. The best tour is then
    selected.

    Args:
        grid: Cost grid
        tour: Initial tour. If None, then a random tour will be generated
        restarts: Number of restarts

    Returns:
        Best tour found after x restarts
    """
    bestTour = runHillClimbing(grid, tour)
    for i in xrange(restarts - 1):
        nextTour = runHillClimbing(grid)
        if nextTour[0] < bestTour[0]:
            bestTour = nextTour
    return bestTour


def scheduleFunction3(time):
    """
    Schedule function for simulated annealing

    Args:
        time: Current iteration count

    Returns:
        Calculated schedule value
    """
    return 2500 * exp(-0.0000002 * time**2 - 0.000001*time)


def scheduleFunction2(time):
    """
    Schedule function for simulated annealing

    Args:
        time: Current iteration count

    Returns:
        Calculated schedule value
    """

    return 2500 - 0.0002 * time**2


def scheduleFunction(time):
    """
    Schedule function for simulated annealing

    Args:
        time: Current iteration count

    Returns:
        Calculated schedule value
    """
    return 2500 - time


def runSimulatedAnnealing(grid, tour=None, scheduleFunction=scheduleFunction3):
    """
    Runs simulated annealing algorithm to minimize cost for TSP.

    Basically keep searching until the calculated time value equals 0.

    The probability of accepting a worse cost depends on the schedule function
    and the difference in the best cost and the new cost.

    If the cost is better, that tour will be accepted regardless.

    Args:
        grid: Cost matrix to use
        scheduleFunction: Schedule function to use. Make sure function eventaully reaches 0!

    Returns:
        Best cost found
    """
    k = 2
    tour = tour if tour is not None else generateTour(len(grid))
    bestTour = [calcCost(tour, grid), tour]
    nextTour = bestTour
    t = 0
    while True:
        T = scheduleFunction(t)
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


def printTour(tour, grid, cityNames):
    """
    Prints the tour and costs

    Args:
        tour: The tour to print
        grid: The cost matrix used to calculate tour cost
        cityNames: Names of cities that correspond to integer values in tour list
    """
    totalCost = calcCost(tour, grid)
    start = tour[0]
    stopCount = 1
    for dest in tour[1:]:
        print ''.join([str(stopCount), '. ', cityNames[start], '/', cityNames[dest], '(', str(grid[start][dest]), ')'])
        start = dest
        stopCount += 1
    print ''.join([str(stopCount), '. ', cityNames[tour[-1]], '/', cityNames[0], '(', str(grid[tour[-1]][0]), ')'])
    print "----------------------------"
    print ''.join(['Total Cost: ', str(totalCost)])


def main():

    # Settings
    seedValue = 10
    n = 10
    restarts = 50

    if seedValue:
        seed(seedValue)

    cityNames = getCityNames()
    costGrid = generateCostGrid(n)
    initialTour = generateTour(len(costGrid))
    initialCost = calcCost(initialTour, costGrid)

    print "Settings:"
    print "----------------------------"
    print ''.join(['Control Parameters: SEED = ', str(seedValue), ', CITIES = ', str(n), "\n"])

    print "Cost Matrix:"
    print "----------------------------"
    printCostGrid(costGrid)

    print "\nInitial Tour:"
    print "----------------------------"
    printTour(initialTour, costGrid, cityNames)

    bestTourRandomRestart = runRandomRestartHillClimbing(costGrid, initialTour, restarts)
    print ''.join(["\nBest Tour using Random Restart (", str(restarts), ' restarts):'])
    print "----------------------------"
    printTour(bestTourRandomRestart[1], costGrid, cityNames)

    bestTourSimulatedAnnealing = runSimulatedAnnealing(costGrid, initialTour, scheduleFunction)
    print "\nBest Tour using Simulated Annealing with schedule cost: 2500 - t"
    print "----------------------------"
    printTour(bestTourSimulatedAnnealing[1], costGrid, cityNames)

    bestTourSimulatedAnnealing = runSimulatedAnnealing(costGrid, initialTour, scheduleFunction2)
    print "\nBest Tour using Simulated Annealing with schedule cost: 2500 - 0.0002 * t^2"
    print "----------------------------"
    printTour(bestTourSimulatedAnnealing[1], costGrid, cityNames)

    bestTourSimulatedAnnealing = runSimulatedAnnealing(costGrid, initialTour, scheduleFunction3)
    print "\nBest Tour using Simulated Annealing with schedule cost: 2500 * e^(-0.0000002 * t^2 - 0.000001*t)"
    print "----------------------------"
    printTour(bestTourSimulatedAnnealing[1], costGrid, cityNames)

if __name__ == '__main__':
    main()