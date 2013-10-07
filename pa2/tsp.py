import csv
import random
import time

from math import exp, expm1, floor, cos, ceil


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


def generateCostGrid(n=10, min=100, max=2500, randint=None):
    """
    Generates a 2-d array to use as the cost grid.

    Args:
        n: The size of the cost grid. Creates an n x n matrix
        min: Minimum cost. Inclusive. Should be less than max cost
        max: Maximum cost. Inclusive.
        randint: Pass in instance of randint to override global randint function
    """
    if randint is None:
        randint = random.randint
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
    random.shuffle(tour)
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


def scheduleFunction5(time):
    """
    Schedule function for simulated annealing

    Args:
        time: Current iteration count

    Returns:
        Calculated schedule value
    """
    if (time == 2000):
        return 0
    else:
        T = ceil(2500 * exp(-.002 * time) * cos(.1 * time))
        if T > 0:
            return T
        else:
            return 1


def scheduleFunction4(time):
    """
    Schedule function for simulated annealing

    Args:
        time: Current iteration count

    Returns:
        Calculated schedule value
    """
    return floor(1250.0 * cos(1/2500.0 * float(time)) + 1250)


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
        random.shuffle(tourPermutations)
        for currentTour in tourPermutations:
            if currentTour[0] <= nextTour[0]:
                nextTour = currentTour
                if nextTour[0] < bestTour[0]:
                    bestTour = nextTour
                break
            else:
                result = abs(currentTour[0] - nextTour[0])/T
                if result < 13 and 1/exp(result) >= random.random():
                    nextTour = currentTour
                    if nextTour[0] < bestTour[0]:
                        bestTour = nextTour
                    break
        t += 1
    return bestTour


def printTour(tour, grid, cityNames, elapsed=None):
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
    if elapsed is not None:
        print ''.join(['Total Time: ', str(elapsed)])


def main():

    # Settings
    csvOutput = False
    basefile = "results"
    costSeed = 10
    runs = 5
    globalSeed = 1000
    n = 10
    min=100
    max=2500
    # End Settings


    if globalSeed:
        random.seed(globalSeed)

    cityNames = getCityNames()

    costRand = random.Random()
    costRand.seed(costSeed)

    costGrid = generateCostGrid(n, min, max, costRand.randint)

    algorithms = [
        {
            "title": "Hill Climbing",
            "algorithm": lambda it: runHillClimbing(costGrid, it)
        },
        {
            "title": "Random Restart: 50",
            "algorithm": lambda it: runRandomRestartHillClimbing(costGrid, it, 50)
        },
        {
            "title": "Random Restart: 100",
            "algorithm": lambda it: runRandomRestartHillClimbing(costGrid, it, 100)
        },
        {
            "title": "Random Restart: 150",
            "algorithm": lambda it: runRandomRestartHillClimbing(costGrid, it, 150)
        },
        {
            "title": "Random Restart: 300",
            "algorithm": lambda it: runRandomRestartHillClimbing(costGrid, it, 300)
        },
        {
            "title": "Simulated Annealing: 2500 - t",
            "algorithm": lambda it: runSimulatedAnnealing(costGrid, it, scheduleFunction)
        },
        {
            "title": "Simulated Annealing: 2500 - 0.0002 * t^2",
            "algorithm": lambda it: runSimulatedAnnealing(costGrid, it, scheduleFunction2)
        },
        {
            "title": "Simulated Annealing: 2500 * e^(-0.0000002 * t^2 - 0.000001*t)",
            "algorithm": lambda it: runSimulatedAnnealing(costGrid, it, scheduleFunction3)
        },
        {
            "title": "Simulated Annealing: floor(1250 * cos(1/2500 * t) + 1250)",
            "algorithm": lambda it: runSimulatedAnnealing(costGrid, it, scheduleFunction4)
        },
        {
            "title": "Simulated Annealing: ceil(2500 * exp(-.02 * time) * cos(.1 * time)",
            "algorithm": lambda it: runSimulatedAnnealing(costGrid, it, scheduleFunction4)
        },
    ]

    results = []
    for i in xrange(runs):
        algoResults = []

        initialTour = generateTour(len(costGrid))
        initialCost = calcCost(initialTour, costGrid)

        for algo in algorithms:
            start = time.time()
            bestTour = algo['algorithm'](initialTour)
            elapsed = (time.time() - start)
            algoResults.append({
                "title": algo["title"],
                "best": bestTour[1],
                "cost": bestTour[0],
                "elapsed": elapsed
            })

        results.append({
            "data": algoResults,
            "initialTour": initialTour,
            "initialCost": initialCost
        })


    print "Settings:"
    print "----------------------------"
    print ''.join(['Control Parameters: COST_SEED = ', str(costSeed), ', CITIES = ', str(n), "\n"])

    print "Cost Matrix:"
    print "----------------------------"
    printCostGrid(costGrid)

    runCount = 1
    for runResult in results:
        data = runResult['data']
        initialTour = runResult['initialTour']
        initialCost = runResult['initialCost']

        print ''.join(["\n\nRun: ", str(runCount)])
        print "============================\n"
        initialTour = generateTour(len(costGrid))
        initialCost = calcCost(initialTour, costGrid)

        print "\nInitial Tour:"
        print "----------------------------"
        printTour(initialTour, costGrid, cityNames)

        for algoResult in data:
            print ''.join(["\n", algoResult['title']])
            print "----------------------------"
            printTour(algoResult['best'], costGrid, cityNames, algoResult['elapsed'])

        runCount += 1


    if csvOutput:
        runCount = 1
        filename = ''.join([basefile, str(costSeed), '.csv'])
        with open(filename, 'w') as csvfile:
            resultWriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for runResult in results:
                data = runResult['data']
                initialTour = runResult['initialTour']
                initialCost = runResult['initialCost']
                resultWriter.writerow(["Run", "Initial Tour", "Initial Cost"])
                resultWriter.writerow([str(runCount), str(initialTour), initialCost])
                resultWriter.writerow(["Algorithm", "Best Tour", "Cost", "Elapsed"])
                for algoResult in data:
                    resultWriter.writerow([
                         str(algoResult['title']),
                         str(algoResult['best']),
                         algoResult['cost'],
                         algoResult['elapsed']
                    ])
                runCount += 1


if __name__ == '__main__':
    main()