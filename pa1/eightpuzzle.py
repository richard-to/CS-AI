import heapq
import itertools
import random
import time

class PuzzleState(object):
    """
    The current puzzle state, its cost, and its last state

    Attributes:
        state: State of the 8-puzzle
        cost: Cost of the 8-puzzle. Defaults to 1
        goal: Goal State
        last: Reference to last puzzle state. If no last state, then is start state
        blank: Value of blank title. Defaults to 0
    """

    def __init__(self, state=None, last=None, goal=None, cost=1, blank=0):
        self.state = state
        self.last = last
        self.goal = goal
        self.cost = cost
        self.blank = blank
        self.stepCost = None
        self.sideLen = len(state)
        self.sides = range(self.sideLen)
        self.blankPos = self.findBlankPos()
        self.pathCost = self.calcPathCost()

    def slideUp(self):
        return self.swap(self.blankPos[0], self.blankPos[1] - 1)

    def slideDown(self):
        return self.swap(self.blankPos[0], self.blankPos[1] + 1)

    def slideLeft(self):
        return self.swap(self.blankPos[0] - 1, self.blankPos[1])

    def slideRight(self):
        return self.swap(self.blankPos[0] + 1, self.blankPos[1])

    def validPos(self, col, row):
        """
        Checks if col/row pair are valid positions in puzzle

        Attributes:
            col: Column index
            row: Row index
        """
        return (0 <= col < self.sideLen and 0 <= row < self.sideLen)

    def swap(self, col, row):
        """
        Swaps blank position with new position and
        creates a new puzzle state

        This is an private method and should not be
        called directly.

        Attributes:
            col: Column index to swap with blank column
            row: Row index to swap with blank row

        Returns:
            PuzzleState object with new state, updated cost,
            reference to old PuzzleState.

            If invalid swap, then `None` will be returned
        """
        if not self.validPos(col, row):
            return None
        currentState = self.state
        newState = [list(r) for r in currentState]
        newState[self.blankPos[0]][self.blankPos[1]] = newState[col][row]
        newState[col][row] = self.blank
        newState = tuple(itertools.imap(tuple, newState))

        nextPuzzleState = PuzzleState(newState, self, self.goal)
        return nextPuzzleState

    def isGoal(self):
        """
        Checks whether this state is a goal state
        """
        return self == self.goal

    def predictedCost(self):
        """
        Returns a predicated cost which is calculated
        differently based on calcStepCost and calcPathCost
        algorithm implements.

        By default uniform cost search is used. For the 8-puzzle,
        this is basically breadth-first search.

        Returns:
            Heuristic cost
        """
        return self.pathCost + self.calcStepCost()

    def hueristic(self):
        return 0

    def calcStepCost(self):
        """
        Calculates step cost using heuristic method. Default just
        returns 0
        """
        if not self.stepCost:
            self.stepCost = self.hueristic()
        return self.stepCost

    def calcPathCost(self):
        """
        Calculates cost leading up to this state.
        """
        pathCost = 0
        if self.last:
            pathCost = self.cost + self.last.pathCost
        return pathCost

    def hasLast(self):
        """
        Checks if puzzle has a previous state. Can be used
        to check for start state

        Returns:
            True if contains a previous state. False if not
        """
        return self.last is not None

    def printState(self):
        """
        Prints out puzzle state one row per line to improve
        readability
        """
        for row in self.state:
            print row

    def parity(self):
        """
        Calculates if parity is odd or even for puzzle state

        Returns:
            True if odd and false if even
        """
        parity = 0
        stateList = list(itertools.chain(*self.state))
        stateList.remove(0)
        while len(stateList) > 0:
            state = stateList.pop(0)
            for state2 in stateList:
                if state > state2:
                    parity += 1
        return bool(parity % 2)

    def findBlankPos(self):
        """
        Finds the position of the blank tile

        Returns:
            List with col and row position of blank tile in puzzle
            Example: [0, 1]
        """
        state = self.state
        sides = self.sides
        blank = self.blank
        for y in sides:
            for x in sides:
                if state[y][x] == blank:
                    return [y, x]
        raise Exception('Blank tile not found!')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.state == other.state
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.state.__hash__()


class PuzzleStateQueue:
    """
    Priority Queue to keep track of the next best node
    to visit.

    Puzzle states are sorted by lowest predicted cost.

    Args:
        counter: Counter increments as new states added. Used for tie breaker
        states: A sorted list of puzzle states
    """

    def __init__(self):
        self.counter = 0
        self.states = []

    def empty(self):
        """
        Checks if there are any puzzles states in the queue

        Returns:
            True/False
        """
        return len(self.states) == 0

    def add(self, state):
        """
        Adds a new puzzle states to the queue

        Attributes:
            state: The PuzzleState to be added to queue
        """
        self.counter += 1
        heapq.heappush(self.states, (state.predictedCost(), self.counter, state))

    def next(self):
        """
        The next best PuzzleState to try

        Returns:
            The next PuzzleState or None if queue is empty
        """
        try:
            result = heapq.heappop(self.states)
            return result[2]
        except IndexError:
            return None


def genRandPuzzle(side=3):
    """
    Randomly generates a valid 8-puzzle
    with start and goal states.

    Function will loop until a valid puzzle is found.

    Larger puzzles could be generated by changing the side
    value, but this is untested.

    Attributes:
        side: Number of tiles per side. Total size would be side * side

    Returns:
        The starting puzzle state. For example:

        (
            (7, 2, 4),
            (5, 0, 6),
            (8, 3, 1)
        )
    """
    size = side * side

    while True:
        start = range(size)
        random.shuffle(start)
        startState = (start[i:i + side] for i in xrange(0, size, side))
        startState = tuple(itertools.imap(tuple, startState))
        startState = PuzzleState(startState)

        goal = range(size)
        random.shuffle(goal)
        goalState = (goal[i:i + side] for i in xrange(0, size, side))
        goalState = tuple(itertools.imap(tuple, goalState))
        goalState = PuzzleState(goalState)

        if startState.parity() == goalState.parity():
            startState.goal = goalState
            return startState


def manhattanHueristic(self):
    """
    Calculates the distance from the goal for every tile.
    Uses manhattan distance.

    Does not include 0 or blank tile.

    Returns:
        Number of tiles still out of place
    """
    count = 0
    startState = self.state
    goalState = self.goal.state
    sides = self.sides

    sideCount = len(sides)
    goalY = range(sideCount * sideCount)
    goalX = range(sideCount * sideCount)
    for y in sides:
        for x in sides:
            goalY[goalState[y][x]] = y
            goalX[goalState[y][x]] = x

    for y in sides:
        for x in sides:
            tile = startState[y][x]
            if tile != 0 and tile != goalState[y][x]:
                count += abs(goalX[tile] - x) + abs(goalY[tile] - y)
    return count


def misplacedTilesHueristic(self):
    """
    Misplaced tiles heuristic. Added cost is the
    number of tiles that are out of place still.

    Does not include 0 or blank tile.

    Returns:
        Number of tiles still out of place
    """
    count = 0
    startState = self.state
    goalState = self.goal.state
    sides = self.sides
    for y in sides:
        for x in sides:
            tile = startState[y][x]
            if tile != 0 and tile != goalState[y][x]:
                count += 1
    return count


def greedyCost(self):
    """
    Uses greedy best first search algorithm instead
    of uniform cost search to calculate predictedCost.

    Essentially only the step cost will be returned.

    Returns:
        Predicated cost value.
    """
    return self.calcStepCost()


def main():
    visited = set()

    #PuzzleState.hueristic = misplacedTilesHueristic
    #PuzzleState.hueristic = manhattanHueristic
    #PuzzleState.predictedCost = greedyCost
    startState = genRandPuzzle()

    startState = PuzzleState((
        (7, 2, 4),
        (5, 0, 6),
        (8, 3, 1)
    ))
    goalState = PuzzleState((
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8)
    ))
    startState.goal = goalState

    queue = PuzzleStateQueue()
    queue.add(startState)

    maxIterations = 200000
    iteration = 0
    endState = None
    start = time.time()
    while iteration < maxIterations and not endState and not queue.empty():
        currentState = queue.next()
        if currentState not in visited:
            visited.add(currentState)
            if currentState.isGoal():
                endState = currentState
            else:
                actions = [currentState.slideUp, currentState.slideDown,
                    currentState.slideLeft, currentState.slideRight]
                for action in actions:
                    newState = action()
                    if newState:
                        queue.add(newState)
            iteration += 1
    elapsed = (time.time() - start)

    print ':'.join(['Iterations', str(iteration)])
    print ':'.join(['Elapsed', str(elapsed)])

    print "Start State:"
    startState.printState()
    print "Goal State:"
    startState.goal.printState()
    print "Final State:"
    endState.printState()

    path = []
    pathState = endState
    while pathState.last:
        path.insert(0, pathState)
        pathState = pathState.last

    print "Moves:"
    for i in xrange(len(path)):
        print i + 1
        path[i].printState()


if __name__ == '__main__':
    main()
