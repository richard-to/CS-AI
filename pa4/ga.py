import random
import time

ITEM_WEIGHT = 0
ITEM_VALUE = 1
FITNESS = 0
KNAPSACK = 1
NOT_IN_KNAPSACK = 0
IN_KNAPSACK = 1
DEFAULT_FITNESS = 0

class KnapsackGA:
    def __init__(self, objList, maxWeight, crossoverPct, mutationPct):
        self.crossoverPct = crossoverPct
        self.mutationPct = mutationPct
        self.objList = objList
        self.maxWeight = maxWeight
        self.numObj = len(self.objList)

    def calcFitness(self, knapsack):
        weight = 0
        value = 0
        for i in xrange(self.numObj):
            if knapsack[i] == IN_KNAPSACK:
                weight += self.objList[i][ITEM_WEIGHT]
                value += self.objList[i][ITEM_VALUE]
        if weight > self.maxWeight:
            value = 0
        return value

    def genInitialPop(self, popSize, items=100):
        population = []
        objIndex = xrange(self.numObj)
        for i in xrange(popSize):
            knapsack = [NOT_IN_KNAPSACK] * self.numObj
            pickedItems = random.sample(objIndex, items)
            for itemIndex in pickedItems:
                knapsack[itemIndex] = IN_KNAPSACK
            value = self.calcFitness(knapsack)
            population.append([value, knapsack])
        return population

    def tournamentSelection(self, population):
        popSize = len(population)
        newPopulation = []
        for i in xrange(popSize):
            genome1 = population[random.randint(0, popSize - 1)]
            genome2 = population[random.randint(0, popSize - 1)]
            if genome1[FITNESS] > genome2[FITNESS]:
                newPopulation.append([genome1[FITNESS], genome1[KNAPSACK][:]])
            else:
                newPopulation.append([genome2[FITNESS], genome2[KNAPSACK][:]])
        return newPopulation

    def crossover(self, population):
        popSize = len(population) / 2
        newPop = []
        for i in xrange(popSize):
            genome1 = population[i * 2]
            genome2 = population[i * 2 + 1]
            if random.random() < self.crossoverPct:
                newPop.extend(self._crossover(genome1, genome2))
            else:
                newPop.append(genome1)
                newPop.append(genome2)

        if newPop < len(population):
            newPop.append(population[-1])

        return newPop

    def _crossover(self, genome1, genome2):
        cPoint = random.randint(1, self.numObj - 2)

        knapsack1 = genome1[KNAPSACK][0:cPoint] + genome1[KNAPSACK][cPoint:]
        value1 = self.calcFitness(knapsack1)

        knapsack2 = genome2[KNAPSACK][0:cPoint] + genome2[KNAPSACK][cPoint:]
        value2 = self.calcFitness(knapsack2)

        return [
            [value1, knapsack1],
            [value2, knapsack2]
        ]

    def mutate(self, population):
        return [self._mutate(genome) for genome in population]

    def _mutate(self, genome):
        knapsack = genome[KNAPSACK][:]
        for i in xrange(self.numObj):
            if random.random() < self.mutationPct:
                if knapsack[i] == IN_KNAPSACK:
                    knapsack[i] = NOT_IN_KNAPSACK
                else:
                    knapsack[i] = IN_KNAPSACK
        value = self.calcFitness(knapsack)
        return [value, knapsack]

    def survivorSelection(self, oldPop, newPop):
        popSize = len(oldPop)
        nextGen = oldPop[:]
        nextGen.extend(newPop)
        nextGen = sorted(nextGen, key=lambda genome: genome[FITNESS], reverse=True)
        return nextGen[:popSize]

    def pickBest(self, population):
        bestGenome = population[0]
        for genome in population:
            if genome[FITNESS] > bestGenome[FITNESS]:
                bestGenome = genome
        return bestGenome

    def printPop(self, population):
        for genome in population:
            print genome


def createObjList(rand, nItems, mWeight, mValue):
    return [[rand.randint(1, mWeight), rand.randint(1, mValue)] for i in xrange(nItems)]


def main():
    seed = 10
    numIterations = 3000
    numItems = 1000
    maxItemValue = 500
    maxItemWeight = 50

    maxWeight = 2500
    popSize = 100
    crossoverPct = 0.80
    mutationPct = 0.05

    rand = random.Random()
    if seed > 0:
        rand.seed(seed)

    objList = createObjList(rand, numItems, maxItemWeight, maxItemValue)
    knapsackGA = KnapsackGA(objList, maxWeight, crossoverPct, mutationPct)
    population = knapsackGA.genInitialPop(popSize)
    currentGen = 0
    startTime = time.time()
    while currentGen < numIterations:
        newPop = knapsackGA.tournamentSelection(population)
        newPop = knapsackGA.crossover(newPop)
        newPop = knapsackGA.mutate(newPop)
        population = knapsackGA.survivorSelection(population, newPop)
        currentGen += 1
    bestGenome = knapsackGA.pickBest(population)
    print time.time() - startTime
    print bestGenome[FITNESS]


if __name__ == '__main__':
    main()
