import random

def genInitialPop(popSize, maxWeight, objList):
    n = len(objList)
    population = []
    for i in xrange(popSize):
        knapsack = [0] * n
        value = 0
        weight = 0
        for g in xrange(n):
            knapsack[g] = random.randint(0, 1)
            if knapsack[g] > 0:
                weight += objList[g][0]
                value += objList[g][1]
        if weight > maxWeight:
            value = 0
        population.append([value, knapsack])
    return population


def mutate(parent1, mutationPct, maxWeight, objList):
    child1 = parent1[1][:]
    child1Weight = 0
    child1Value = 0

    for i in xrange(child1):
        if random.random() < mutationPct:
            if child1[i] == 0:
                child1[i] = 1
            else:
                child1[i] = 0

    for i in xrange(child1):
        if child1[i] > 0:
            child1Weight += objList[i][0]
            child1Value += objList[i][1]

    if child1Weight > maxWeight:
        child1Value = 0
    return [child1Value, child1]


def crossover(parent1, parent2, maxWeight, objList):
    cPoint = random.randint(1, len(objList) - 2)

    child1 = parent1[1][0:cPoint] + parent2[1][cPoint:]
    child1Value = 0
    child1Weight = 0

    child2 = parent2[1][0:cPoint] + parent1[1][cPoint:]
    child2Value = 0
    child2Weight = 0

    for i in xrange(objList):
        if child1[i] > 0:
            child1Weight += objList[i][0]
            child1Value += objList[i][1]

        if child2[i] > 0:
            child2Weight += objList[i][0]
            child2Value += objList[i][1]

    if child1Weight > maxWeight:
        child1Value = 0

    if child2Weight > maxWeight:
        child2Value = 0

    return [
        [child1Value, child1],
        [child2Value, child2]
    ]


def main():
    random.seed(10)
    numIterations = 10
    maxWeight = 100
    popSize = 3
    mutationPct = 0.1
    objList = [
        [45, 3],
        [40, 5],
        [50, 8],
        [90, 10]
    ]
    print len(objList)-2

    population = genInitialPop(popSize, maxWeight, objList)
    print population

    crossover(population[0], population[1], maxWeight, objList)


if __name__ == '__main__':
    main()