import itertools

from copy import deepcopy

def main():
    cost = 1

    visited = set()
    states = []

    actions = (
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0)
    )

    startState = (
        (7, 2, 4),
        (5, 0, 6),
        (8, 3, 1)
    )

    goalState = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8)
    )

    states.insert(0, startState)
    visited.add(startState)

    found = False
    iteration = 0
    while iteration < 200000 and found is False and len(states) > 0:

        currentState = states.pop()
        if currentState == goalState:
            print iteration
            for row in currentState:
                print row
            found = True
        else:
            for y in xrange(len(currentState)):
                for x in xrange(len(currentState[y])):
                    if currentState[y][x] == 0:
                        pos = [y, x]

            for coord in actions:
                newY = pos[0] + coord[0]
                newX = pos[1] + coord[1]
                if (newY >= 0 and newY < len(currentState) and newX >= 0 and newX < len(currentState[0])):
                    newState = [list(row) for row in currentState]
                    tempVal = newState[pos[0]][pos[1]]
                    newState[pos[0]][pos[1]] = newState[newY][newX]
                    newState[newY][newX] = tempVal
                    newState = tuple(itertools.imap(tuple, newState))
                    if newState not in visited:
                        visited.add(newState)
                        states.insert(0, newState)
        iteration += 1


if __name__ == '__main__':
    main()