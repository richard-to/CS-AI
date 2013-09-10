import itertools
import random
import time

class PuzzleState:
    """
    The current puzzle state, its cost, and its last state

    Attributes:
        state: State of the 8-puzzle
        cost: Cost of the 8-puzzle. Defaults to 1
        last: Reference to last puzzle state. If no last state, then is start state
        blank: Value of blank title. Defaults to 0
    """

    def __init__(self, state=None, last=None, cost=1, blank=0):
        self.state = state
        self.last = last
        self.cost = cost
        self.blank = blank
        self.sideLen = len(state)
        self.sides = range(self.sideLen)
        self.blankPos = self.findBlankPos()

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
        """
        return (0 <= col < self.sideLen and 0 <= row < self.sideLen)

    def swap(self, col, row):
        """
        Swaps blank position with new position and
        creates a new puzzle state

        This is an private method and should not be
        called directly.

        Args:
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

        nextPuzzleState = PuzzleState(newState, self)
        nextPuzzleState.addCost(self.cost)
        return nextPuzzleState

    def addCost(self, cost):
        """
        Adds puzzle cost to base cost

        Args:
            cost: Cost to add to current cost
        """
        self.cost += cost

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
        return True

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

def genRandPuzzle():
    """
    Randomly generates a valid 8-puzzle
    with start and goal states.

    Returns:
        A list with a start state and goal state. For example:

        [
            (
                (7, 2, 4),
                (5, 0, 6),
                (8, 3, 1)
            ),
            (
                (0, 1, 2),
                (3, 4, 5),
                (6, 7, 8)
            )
        ]
    """
    side = 3
    size = side * side

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
        return [startState, goalState]
    else:
        return False


def main():
    visited = set()
    states = []

    #startState, goalState = genRandPuzzle()
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

    states.insert(0, startState)
    visited.add(startState)

    maxIterations = 200000
    iteration = 0
    found = False
    start = time.time()
    while iteration < maxIterations and not found and states:
        print iteration
        #states = sorted(states, key=lambda state: state.cost, reverse=True)
        currentState = states.pop()
        if currentState == goalState:
            currentState.printState()
            found = True
        else:
            actions = [currentState.slideLeft, currentState.slideRight,
                currentState.slideUp, currentState.slideDown]
            for action in actions:
                newState = action()
                if newState and newState not in visited:
                    visited.add(newState)
                    states.insert(0, newState)
        iteration += 1
    elapsed = (time.time() - start)
    print start
    print elapsed

if __name__ == '__main__':
    main()
