import argparse
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
    """
    Genetic algorithm that attempts to solve knapsack problem.

    Attributes:
        objList: List of objects. Each object contains weight and value.
        maxWeight: Maximum weight that knapsack can hold.
        crossoverPct: Crossover rate. Between 0.0-1.0.
        mutationPct: Mutation rate. Between 0.0-1.0.
    """

    def __init__(self, objList, maxWeight, crossoverPct, mutationPct):
        self.crossoverPct = crossoverPct
        self.mutationPct = mutationPct
        self.objList = objList
        self.maxWeight = maxWeight
        self.numObj = len(self.objList)

    def _calcFitness(self, knapsack):
        """
        Calculate fitness for a knapsack. Fitness is the value
        of items in the knapsack. If knapsack is overweight, then
        fitness defaults to 0.

        Note that the knapsack is not the same as the genome. The knapsack
        is the second element in the genome.

        Args:
            knapsack: List of 1s and 0s. 1 if item in knapsack and 0 if not.

        Returns:
            Fitness of knapsack.
        """
        weight = 0
        value = 0
        for i in xrange(self.numObj):
            if knapsack[i] == IN_KNAPSACK:
                weight += self.objList[i][ITEM_WEIGHT]
                value += self.objList[i][ITEM_VALUE]
        if weight > self.maxWeight:
            value = 0
        return value

    def calcWeight(self, genome):
        """
        Calculates the weight of the genome

        Args:
            genome: Array with 2 elements: fitness and knapsack list

        Returns:
            The weight of the items in the knapsack.
        """
        knapsack = genome[KNAPSACK]
        weight = 0
        for i in xrange(self.numObj):
            if knapsack[i] == IN_KNAPSACK:
                weight += self.objList[i][ITEM_WEIGHT]
        return weight

    def genInitialPop(self, popSize, items=100):
        """
        Generates the initial population for the GA

        Args:
            popSize: Size of population.
            items: Number of items to select for each knapsack.

        Returns:
            List of randomly generated genomes.
        """
        population = []
        objIndex = xrange(self.numObj)
        for i in xrange(popSize):
            knapsack = [NOT_IN_KNAPSACK] * self.numObj
            pickedItems = random.sample(objIndex, items)
            for itemIndex in pickedItems:
                knapsack[itemIndex] = IN_KNAPSACK
            value = self._calcFitness(knapsack)
            population.append([value, knapsack])
        return population

    def tournamentSelection(self, population):
        """
        Randomly select two genomes and select the one with best fitness.

        Args:
            population: A list of genomes.

        Returns:
            A list of genomes selected via tournament selection.
        """
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
        """
        Single point crossover operator.

        Args:
            population: A list of genomes.

        Returns:
            A list of genomes after crossover.
        """
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
        """
        Crosses over two genomes at a randomly selected crossover point.

        Args:
            genome1: Genome selected for crossover.
            genome2: Genome selected for crossover.

        Returns:
            Return genome1 and genome2 after crossover with recalculated fitnesses.
        """
        cPoint = random.randint(1, self.numObj - 2)

        knapsack1 = genome1[KNAPSACK][0:cPoint] + genome1[KNAPSACK][cPoint:]
        value1 = self._calcFitness(knapsack1)

        knapsack2 = genome2[KNAPSACK][0:cPoint] + genome2[KNAPSACK][cPoint:]
        value2 = self._calcFitness(knapsack2)

        return [
            [value1, knapsack1],
            [value2, knapsack2]
        ]

    def mutate(self, population):
        """
        Mutation operator.

        Args:
            population: A list of genomes.

        Returns:
            A list of genomes after mutation.
        """
        return [self._mutate(genome) for genome in population]

    def _mutate(self, genome):
        """
        Go through each allele of genome and randomly test each for
        mutation. Adjust mutation rate accordingly.

        Args:
            genome: Genome to run mutation on.

        Returns:
            Return genome after mutation with recalculated fitnesses.
        """
        knapsack = genome[KNAPSACK][:]
        for i in xrange(self.numObj):
            if random.random() < self.mutationPct:
                if knapsack[i] == IN_KNAPSACK:
                    knapsack[i] = NOT_IN_KNAPSACK
                else:
                    knapsack[i] = IN_KNAPSACK
        value = self._calcFitness(knapsack)
        return [value, knapsack]

    def survivorSelection(self, oldPop, newPop):
        """
        Select genomes with best fitness from old and new populations.

        Args:
            oldPop: List of genomes that began the current generation.
            newPop: List of new genomes after tournament selection, crossover, and mutation.

        Args:
            List of genomes to move on to next generation.
        """
        popSize = len(oldPop)
        nextGen = oldPop[:]
        nextGen.extend(newPop)
        nextGen = sorted(nextGen, key=lambda genome: genome[FITNESS], reverse=True)
        return nextGen[:popSize]

    def pickBest(self, population):
        """
        Pick best genome in population.

        Args:
            population: List of genomes.

        Returns:
            Genome with best fitness.
        """
        bestGenome = population[0]
        for genome in population:
            if genome[FITNESS] > bestGenome[FITNESS]:
                bestGenome = genome
        return bestGenome

    def printPop(self, population):
        for genome in population:
            print genome


def createObjList(rand, nItems, mWeight, mValue):
    """
    Creates an object list of items with weights and values.

    Args:
        rand: Random object specifically for creating object list.
        nItems: Number of items to generate.
        mWeight: Maximum weight of items.
        mValue: Maximum value of an item.

    Returns:
        List of objects with weights and values. Example:

        [
            [25, 150],
            [55, 190],
            [99, 345],
        ]
    """
    return [[rand.randint(1, mWeight), rand.randint(1, mValue)] for i in xrange(nItems)]


def main():
    parser = argparse.ArgumentParser(description='Run GA for knapsack problem.')
    parser.add_argument('-s', '--seed', type=int, help='Random seed for GA run.')
    parser.add_argument('-o', '--oseed', type=int, help='Random seed for generating objects weights and values.')
    parser.add_argument('-p', '--population', type=int, help='Population size to use.', default=100)
    parser.add_argument('-g', '--generations', type=int, help='Number of generations to run GA.', default=4000)
    parser.add_argument('-c', '--crossover', type=float, help='Crossover rate.', default=0.90)
    parser.add_argument('-m', '--mutation', type=float, help='Mutation rate.', default=0.02)
    args = parser.parse_args()

    seed = args.seed
    oseed = args.oseed
    generations = args.generations
    popSize = args.population
    crossoverPct = args.crossover
    mutationPct = args.mutation

    numItems = 1000
    startingItems = 50
    maxItemValue = 500
    maxItemWeight = 50
    maxWeight = 2500

    if seed is not None:
        random.seed(seed)

    rand = random.Random()
    if oseed is not None:
        rand.seed(oseed)

    objList = createObjList(rand, numItems, maxItemWeight, maxItemValue)
    knapsackGA = KnapsackGA(objList, maxWeight, crossoverPct, mutationPct)
    population = knapsackGA.genInitialPop(popSize, startingItems)

    bestInitialGenome = knapsackGA.pickBest(population)
    initialFitness = bestInitialGenome[FITNESS]
    initialWeight = knapsackGA.calcWeight(bestInitialGenome)

    currentGen = 0
    startTime = time.time()
    while currentGen < generations:
        newPop = knapsackGA.tournamentSelection(population)
        newPop = knapsackGA.crossover(newPop)
        newPop = knapsackGA.mutate(newPop)
        population = knapsackGA.survivorSelection(population, newPop)
        currentGen += 1
    elapsedTime = time.time() - startTime

    bestGenome = knapsackGA.pickBest(population)
    bestFitness = bestGenome[FITNESS]
    bestWeight = knapsackGA.calcWeight(bestGenome)

    print "\nSettings"
    print "---------------------"
    print "GA Seed:", seed
    print "Knapsack Seed:", oseed
    print "Population Size:", popSize
    print "Generations:", generations
    print "Crossover Rate:", crossoverPct
    print "Mutation Rate:", mutationPct

    print "\nBest Initial Genome"
    print "---------------------"
    print "Fitness:", initialFitness
    print "Weight:", initialWeight

    print "\nBest Final Genome:"
    print "---------------------"
    print "Fitness:", bestFitness
    print "Weight:", bestWeight
    print "Runtime:", elapsedTime
    print ""

if __name__ == '__main__':
    main()
